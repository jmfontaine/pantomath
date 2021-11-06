"""Data source for AWS Elastic File System (EFS) file systems."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.sqltypes import Float, Integer

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_efs_file_systems")
class AwsEfsFileSystemsDataSource(AwsDataSource):
    """Data source for AWS Elastic File System (EFS) file systems."""

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) for the EFS file system.",
            hydrate="FileSystemArn",
            name="arn",
        ),
        DataSourceColumn(
            description="The time that the file system was created, in seconds (since 1970-01-01T00:00:00Z).",  # noqa: E501
            hydrate="CreationTime",
            name="creation_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The ID of the file system, assigned by Amazon EFS.",
            hydrate="FileSystemId",
            name="id",
        ),
        DataSourceColumn(
            description="The lifecycle phase of the file system.",
            hydrate="LifeCycleState",
            name="life_cycle_state",
        ),
        DataSourceColumn(
            description="The name the EFS file system.",
            hydrate="Name",
            name="name",
        ),
        DataSourceColumn(
            description="The current number of mount targets that the file system has.",
            hydrate="NumberOfMountTargets",
            name="number_of_mount_targets",
            type=Integer,
        ),
        DataSourceColumn(
            description="The performance mode of the file system.",
            hydrate="PerformanceMode",
            name="performance_mode",
        ),
        DataSourceColumn(
            description="The amount of provisioned throughput, measured in MiB/s, for the file system. ",  # noqa: E501
            hydrate="ProvisionedThroughputInMibps",
            name="provisioned_throughput",
            type=Float,
        ),
        DataSourceColumn(
            description="The latest known metered size (in bytes) of data stored in the file system, in its Value field, and the time at which that size was determined in its Timestamp field.",  # noqa: E501
            hydrate="SizeInBytes",
            name="size_in_bytes",
            type=JSONB,
        ),
        DataSourceColumn(
            description="Any tags assigned to the EFS file system.",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="Displays the file system's throughput mode.",
            hydrate="ThroughputMode",
            name="throughput_mode",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_file_systems",
        "results_filter": "FileSystems[]",
        "service_name": "efs",
    }
