"""Data source for AWS CloudFront distributions."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_cloudfront_distributions")
class AwsCloudfrontDistributionsDataSource(AwsDataSource):
    """Data source for AWS CloudFront distributions."""

    columns = [
        DataSourceColumn(
            description="The information about CNAMEs (alternate domain names), if any, for this distribution.",  # noqa: E501
            hydrate="Aliases.Items",
            name="aliases",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The ARN (Amazon Resource Name) for the distribution.",
            hydrate="ARN",
            name="arn",
        ),
        DataSourceColumn(
            description="The domain name that corresponds to the distribution.",
            hydrate="DomainName",
            name="domain_name",
        ),
        DataSourceColumn(
            description="The date and time the distribution was last modified.",
            hydrate="LastModifiedTime",
            name="last_modified_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The name the distribution.",
            hydrate="tags.Tags[?Key=='Name'] | [0].Value",
            name="name",
        ),
        DataSourceColumn(
            description="The information about origins for this distribution.",
            hydrate="Origins.Items",
            name="origins",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The current status of the distribution.",
            hydrate="Status",
            name="status",
        ),
        DataSourceColumn(
            description="Any tags assigned to the distribution",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "list_tags_for_resource",
            "method_parameters": {"Resource": "{ARN}"},
            "results_filter": '[{"Tags": @.Tags.Items}]',
            "service_name": "cloudfront",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_distributions",
        "results_filter": "DistributionList.Items[]",
        "service_name": "cloudfront",
    }
