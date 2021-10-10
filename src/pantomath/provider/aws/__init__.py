import asyncio
import builtins
import dataclasses
import logging
from copy import Error
from dataclasses import dataclass, field
from typing import Union

import aiobotocore.session
import aiostream
import botocore
import jmespath
from aiostream import operator
from aiostream.pipe import flatmap
from aiostream.stream import flatten
from botocore.config import Config
from sqlalchemy import Column, MetaData, Table

from pantomath.datasource import DataSource, DataSourceColumn
from pantomath.provider import AsyncIteratorWrapper, Provider, providers, to_sqlalchemy
from pantomath.registry import CachedRegistry

data_sources = CachedRegistry()


async def call_botocore_method(
    session,
    account_id,
    region_name,
    service_name,
    method_name,
    add_metadata=True,
    results_filter=None,
    method_parameters=None,
    expected_errors=None,
):
    if not expected_errors:
        expected_errors = []
    if not method_parameters:
        method_parameters = {}

    try:
        config = Config(
            retries={
                "max_attempts": 10,
                "mode": "adaptive",
            }
        )
        async with session.create_client(
            service_name, config=config, region_name=region_name
        ) as client:
            if client.can_paginate(method_name):
                paginator = client.get_paginator(method_name)
                page_iterator = paginator.paginate(**method_parameters)
            else:
                method = getattr(client, method_name)
                response = await method(**method_parameters)
                page_iterator = AsyncIteratorWrapper([response])

            results_filter_expression = jmespath.compile(results_filter)

            async for page in page_iterator:
                items = results_filter_expression.search(page)
                if items is not None:
                    for item in items:
                        if add_metadata:
                            item["metadata"] = {
                                "account_id": account_id,
                                "region": region_name,
                                "session": session,
                            }
                        yield item
    except botocore.exceptions.ClientError as error:
        error_code = error.response["Error"]["Code"]
        if error_code in expected_errors:
            item = {}
            if add_metadata:
                item["metadata"] = {
                    "account_id": account_id,
                    "region": region_name,
                    "session": session,
                }
            yield item
        else:
            raise error
    except Error as error:
        raise error


async def assume_iam_role(iam_role_arn, session):
    async with session.create_client("sts") as sts:
        response = await sts.assume_role(
            RoleArn=iam_role_arn, RoleSessionName="pantomath"
        )

        new_session = aiobotocore.session.AioSession()
        new_session.set_credentials(
            access_key=response["Credentials"]["AccessKeyId"],
            secret_key=response["Credentials"]["SecretAccessKey"],
            token=response["Credentials"]["SessionToken"],
        )

        return new_session


async def get_account_id(session):
    async with session.create_client("sts") as client:
        response = await client.get_caller_identity()

    return response["Account"]


async def get_available_regions(session, service_name):
    # KLUDGE: Some global services need to point to a region.
    if service_name in ["cloudfront", "s3"]:
        return ["us-east-1"]

    service_regions = await session.get_available_regions(
        service_name, partition_name="aws"
    )

    # Unfortunately, Session.get_available_regions() returns all regions
    # the service is available in, ignoring the regions disabled in the account.
    # We need to filter out the disabled regions from the result
    # to get the regions available to us.
    async with session.create_client("ec2", region_name="us-east-1") as client:
        response = await client.describe_regions(
            Filters=[
                {
                    "Name": "opt-in-status",
                    "Values": [
                        "opt-in-not-required",
                        "opted-in",
                    ],
                }
            ],
        )
    account_regions = sorted([r["RegionName"] for r in response["Regions"]])

    return list(set.intersection(*map(set, [service_regions, account_regions])))


async def get_session(account_config):
    session = aiobotocore.session.AioSession(profile=account_config.profile)

    if account_config.assume_role:
        session = await assume_iam_role(account_config.assume_role, session)

    return session  # noqa: R504


def beautify_tags(tags: dict) -> Union[dict, None]:
    if not tags:
        return None

    # KLUDGE: Sadly, some API calls return tags with lower case keys
    if "key" in tags[0]:
        key_name = "key"
        value_name = "value"
    else:
        key_name = "Key"
        value_name = "Value"

    return {tag[key_name]: tag[value_name] for tag in tags}


@operator
async def from_botocore(
    aws_accounts,
    service_name,
    method_name,
    method_parameters=None,
    results_filter=None,
    regions=None,
):
    for aws_account in aws_accounts:
        session = await get_session(aws_account)
        account_id = await get_account_id(session)

        if not regions:
            regions = await get_available_regions(
                session=session, service_name=service_name
            )

        for region in regions:
            yield call_botocore_method(
                session=session,
                account_id=account_id,
                region_name=region,
                service_name=service_name,
                method_name=method_name,
                method_parameters=method_parameters,
                results_filter=results_filter,
            )


@dataclass(frozen=True)
@providers.register("aws")
class AWSProvider(Provider):
    def __post_init__(self):
        super().__post_init__()
        logging.getLogger("botocore").setLevel(self.log_level)

    async def collect(self):
        def _build_table(conn, name, columns, excluded_default_columns):
            table = Table(name, MetaData(bind=conn))

            if "account_id" not in excluded_default_columns:
                columns.append(
                    DataSourceColumn(
                        description="The AWS account ID.",
                        hydrate=jmespath.compile("metadata.account_id"),
                        index=True,
                        name="account_id",
                    )
                )

            if "region" not in excluded_default_columns:
                columns.append(
                    DataSourceColumn(
                        description="The AWS region.",
                        hydrate=jmespath.compile("metadata.region"),
                        index=True,
                        name="region",
                    )
                )

            columns = sorted(columns, key=lambda c: dataclasses.asdict(c)["name"])
            for column in columns:
                table.append_column(
                    Column(
                        column.name,
                        column.type,
                        comment=column.description,
                        index=column.index,
                    )
                )

            return table

        async def process_data_source(name: str, data_source, aws_accounts):
            async with self.db_engine.begin() as conn:
                table = _build_table(
                    columns=data_source.columns,
                    conn=conn,
                    excluded_default_columns=data_source.excluded_default_columns,
                    name=name,
                )
                if await conn.run_sync(table.exists):
                    await conn.run_sync(table.drop)
                await conn.run_sync(table.create)

                pipeline = (
                    flatten(data_source.extract(aws_accounts))
                    | flatmap(data_source.enrich)
                    | flatmap(data_source.transform)
                    | to_sqlalchemy(conn, table)
                )
                try:
                    await pipeline
                except aiostream.core.StreamEmpty:
                    # No results. Ignore.
                    pass

            # KLUDGE: Must yield something so that this function is an async generator
            yield None

        async def get_coros():
            aws_accounts = self.config["settings"]["accounts"]

            for data_source_name in self.config["sources"]:
                data_source = data_sources.get(data_source_name)
                yield process_data_source(
                    name=data_source_name,
                    data_source=data_source,
                    aws_accounts=aws_accounts,
                )

        await flatten(get_coros(), task_limit=20)


class AwsDataSource(DataSource):
    enrich_config: dict = field(default_factory=dict, init=True)
    extract_config: dict = field(default_factory=dict, init=False)

    def __init__(self):
        super().__init__()

        columns = []
        for column in self.columns:
            hydrate = column.hydrate
            if not hydrate.startswith("resource.") and not hydrate.startswith(
                tuple(self.enrich_config)
            ):
                hydrate = f"resource.{hydrate}"

            columns.append(
                DataSourceColumn(
                    description=column.description,
                    hydrate=jmespath.compile(hydrate),
                    index=column.index,
                    name=column.name,
                    transform=column.transform,
                    type=column.type,
                )
            )

        builtins.object.__setattr__(self, "columns", columns)

        if hasattr(self, "__post_init__") and callable(self.__post_init__):
            self.__post_init__()

    async def enrich(self, source):
        # TODO: Properly name this method
        async def wrap_botocore(source, *args, **kwargs):
            # Borrowed from https://stackoverflow.com/a/50815499
            def recursiveMap(something, func, *args, **kwargs):
                if isinstance(something, dict):
                    accumulator = {}
                    for key, value in something.items():
                        accumulator[key] = recursiveMap(value, func, *args, **kwargs)
                    return accumulator
                elif isinstance(something, (list, tuple, set)):
                    accumulator = []
                    for item in something:
                        accumulator.append(recursiveMap(item, func, *args, **kwargs))
                    return type(something)(accumulator)
                else:
                    return func(something, *args, **kwargs)

            def replace_placeholders(value, *args, **kwargs):
                if isinstance(value, str):
                    return value.format(**kwargs)
                else:
                    return value

            if "method_parameters" in kwargs:
                # Replace the placeholders with the item values
                kwargs["method_parameters"] = recursiveMap(
                    kwargs["method_parameters"], replace_placeholders, **source
                )

            kwargs["add_metadata"] = False

            # Return the first element since we are processing a single item at a time
            return [r async for r in call_botocore_method(*args, **kwargs)][0]

        coros = []
        for config in self.enrich_config.values():
            coros.append(
                wrap_botocore(
                    source=source,
                    session=source["metadata"]["session"],
                    account_id=source["metadata"]["account_id"],
                    region_name=source["metadata"]["region"],
                    **config,
                )
            )
        data = await asyncio.gather(*coros)
        output = dict(zip(self.enrich_config.keys(), data))
        output["resource"] = {k: v for k, v in source.items() if k != "metadata"}
        output["metadata"] = source["metadata"]

        yield output

    def extract(self, aws_accounts):
        return from_botocore(aws_accounts=aws_accounts, **self.extract_config)

    async def transform(self, item):
        transformed_item = {}

        for column in self.columns:
            value = column.hydrate.search(item)

            if value is not None and column.transform is not None:
                value = column.transform(value)

            transformed_item[column.name] = value

        yield transformed_item


# These imports must be at the end of the file to avoid dependency issues
from pantomath.provider.aws import (  # noqa: E402,F401
    cloudfront,
    cloudtrail,
    dax,
    docdb,
    dynamodb,
    ebs,
    ec2,
    ecs,
    efs,
    eks,
    elasticache,
    emr,
    es,
    lambda_,
    rds,
    redshift,
    route53,
    s3,
)
