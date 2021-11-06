"""Data source for AWS Lambda functions."""
from typing import Dict, List

import dateutil.parser
from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY, BIGINT, ENUM, JSONB
from sqlalchemy.sql.sqltypes import Integer

from pantomath.provider.aws import AwsDataSource, DataSourceColumn, data_sources


@data_sources.register("aws_lambda_functions")
class AwsLambdaFunctionsDataSource(AwsDataSource):
    """Data source for AWS Lambda functions."""

    columns = [
        DataSourceColumn(
            description="The instruction set architecture that the function supports. Architecture is a string array with one of the valid values.",  # noqa: E501
            hydrate="Architectures",
            name="architectures",
            type=ARRAY(Text),
        ),
        DataSourceColumn(
            description="The ARN of the function.",
            hydrate="FunctionArn",
            name="arn",
        ),
        DataSourceColumn(
            description="The size of the function's deployment package, in bytes.",
            hydrate="CodeSize",
            name="code_size",
            type=BIGINT,
        ),
        DataSourceColumn(
            description="The function's description.",
            hydrate="Description",
            name="description",
        ),
        DataSourceColumn(
            description="The date and time that the function was last updated, in ISO-8601 format (YYYY-MM-DDThh:mm:ss.sTZD).",  # noqa: E501
            hydrate="LastModified",
            name="last_modified",
            transform=dateutil.parser.parse,
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The status of the last update that was performed on the function.",  # noqa: E501
            hydrate="LastUpdateStatus",
            name="last_update_status",
        ),
        DataSourceColumn(
            description="The reason for the last update that was performed on the function.",  # noqa: E501
            hydrate="LastUpdateStatusReason",
            name="last_update_status_reason",
        ),
        DataSourceColumn(
            description="The amount of memory available to the function at runtime.",
            hydrate="MemorySize",
            name="memory_size",
            type=BIGINT,
        ),
        DataSourceColumn(
            description="The name of the function.",
            hydrate="FunctionName",
            name="name",
        ),
        DataSourceColumn(
            description="The type of deployment package. Set to Image for container image and set Zip for .zip file archive.",  # noqa: E501
            hydrate="PackageType",
            name="package_type",
            type=ENUM(
                "Image",
                "Zip",
                name="aws_lambda_functions_package_type_enum",
            ),
        ),
        DataSourceColumn(
            description="The runtime environment for the Lambda function.",
            hydrate="Runtime",
            name="runtime",
        ),
        DataSourceColumn(
            description="The current state of the function.",
            hydrate="State",
            name="state",
        ),
        DataSourceColumn(
            description="The reason for the function's current state.",
            hydrate="StateReason",
            name="state_reason",
        ),
        DataSourceColumn(
            description="Any tags assigned to the function.",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The amount of time in seconds that Lambda allows a function to run before stopping it.",  # noqa: E501
            hydrate="Timeout",
            name="timeout",
            type=Integer,
        ),
        DataSourceColumn(
            description="The function's networking configuration.",
            hydrate="VpcConfig",
            name="vpc_config",
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "list_tags",
            "method_parameters": {"Resource": "{FunctionArn}"},
            "results_filter": '[{"Tags": @.Tags}]',
            "service_name": "lambda",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_functions",
        "results_filter": "Functions[]",
        "service_name": "lambda",
    }
