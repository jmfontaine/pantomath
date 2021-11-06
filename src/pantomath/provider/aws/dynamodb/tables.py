"""Data source for AWS DynamoDB tables."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import BIGINT, ENUM, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_dynamodb_tables")
class AwsDynamodbTablesDataSource(AwsDataSource):
    """Data source for AWS DynamoDB tables."""

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) that uniquely identifies the table.",  # noqa: E501
            hydrate="table.TableArn",
            name="arn",
        ),
        DataSourceColumn(
            description="The details for the read/write capacity mode.",
            hydrate="table.BillingModeSummary",
            name="billing_mode_summary",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The date and time when the table was created, in UNIX epoch time format.",  # noqa: E501
            hydrate="table.CreationDateTime",
            name="creation_date_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The number of items in the specified table. DynamoDB updates this value approximately every six hours. Recent changes might not be reflected in this value.",  # noqa: E501
            hydrate="table.ItemCount",
            name="item_count",
            type=BIGINT,
        ),
        DataSourceColumn(
            description="The name of the table.",
            hydrate="table.TableName",
            name="name",
        ),
        DataSourceColumn(
            description="The provisioned throughput settings for the table.",
            hydrate="table.ProvisionedThroughput",
            name="provisioned_throughput",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The total size of the specified table, in bytes. DynamoDB updates this value approximately every six hours. Recent changes might not be reflected in this value.",  # noqa: E501
            hydrate="table.TableSizeBytes",
            name="size",
            type=BIGINT,
        ),
        DataSourceColumn(
            description="The current state of the table.",
            hydrate="table.TableStatus",
            type=ENUM(
                "ACTIVE",
                "ARCHIVED",
                "ARCHIVING",
                "CREATING",
                "DELETING",
                "INACCESSIBLE_ENCRYPTION_CREDENTIALS",
                "UPDATING",
                name="aws_dynamodb_tables_status_enum",
            ),
            name="status",
        ),
        DataSourceColumn(
            description="The tags currently associated with the table.",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "table": {
            "method_name": "describe_table",
            "method_parameters": {"TableName": "{Name}"},
            "results_filter": "[Table]",
            "service_name": "dynamodb",
        },
        "tags": {
            "method_name": "list_tags_of_resource",
            "method_parameters": {
                "ResourceArn": "arn:aws:dynamodb:{metadata[region]}:{metadata[account_id]}:table/{Name}"  # noqa: E501
            },
            "results_filter": '[{"Tags": @.Tags}]',
            "service_name": "dynamodb",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_tables",
        "results_filter": 'TableNames[].{"Name": @}',
        "service_name": "dynamodb",
    }
