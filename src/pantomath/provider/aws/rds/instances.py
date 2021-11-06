"""Data source for AWS Relational Database Service (RDS) instances."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.sqltypes import Integer

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_rds_instances")
class AwsRdsInstancesDataSource(AwsDataSource):
    """Data source for AWS Relational Database Service (RDS) instances."""

    columns = [
        DataSourceColumn(
            description="Specifies the allocated storage size specified in gibibytes (GiB).",  # noqa: E501
            hydrate="AllocatedStorage",
            name="allocated_storage",
            type=Integer,
        ),
        DataSourceColumn(
            description="Specifies the name of the Availability Zone the DB instance is located in.",  # noqa: E501
            hydrate="AvailabilityZone",
            name="availability_zone",
        ),
        DataSourceColumn(
            description="Specifies the number of days for which automatic DB snapshots are retained.",  # noqa: E501
            hydrate="BackupRetentionPeriod",
            name="backup_retention_period",
            type=Integer,
        ),
        DataSourceColumn(
            description="If the DB instance is a member of a DB cluster, contains the name of the DB cluster that the DB instance is a member of.",  # noqa: E501
            hydrate="DBClusterIdentifier",
            name="db_cluster_identifier",
        ),
        DataSourceColumn(
            description="Contains the name of the compute and memory capacity class of the DB instance.",  # noqa: E501
            hydrate="DBInstanceClass",
            name="db_instance_class",
        ),
        DataSourceColumn(
            description="Contains a user-supplied database identifier. This identifier is the unique key that identifies a DB instance.",  # noqa: E501
            hydrate="DBInstanceIdentifier",
            name="db_instance_identifier",
        ),
        DataSourceColumn(
            description="Specifies the current state of this database.",
            hydrate="DBInstanceStatus",
            name="db_instance_status",
        ),
        DataSourceColumn(
            description="True if Performance Insights is enabled for the DB instance, and otherwise false.",  # noqa: E501
            hydrate="EnabledCloudwatchLogsExports",
            name="enabled_cloudwatch_logs_exports",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The name of the database engine to be used for this DB instance.",  # noqa: E501
            hydrate="Engine",
            name="engine",
        ),
        DataSourceColumn(
            description="Indicates the database engine version.",
            hydrate="EngineVersion",
            name="engine_version",
        ),
        DataSourceColumn(
            description="Provides the date and time the DB instance was created.",
            hydrate="InstanceCreateTime",
            name="instance_create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Specifies the Provisioned IOPS (I/O operations per second) value.",  # noqa: E501
            hydrate="Iops",
            name="iops",
            type=Integer,
        ),
        DataSourceColumn(
            description="License model information for this DB instance.",
            hydrate="LicenseModel",
            name="license_model",
        ),
        DataSourceColumn(
            description="Specifies if the DB instance is a Multi-AZ deployment.",  # noqa: E501
            hydrate="MultiAZ",
            name="multi_az",
            type=Boolean,
        ),
        DataSourceColumn(
            description="True if Performance Insights is enabled for the DB instance, and otherwise false.",  # noqa: E501
            hydrate="PerformanceInsightsEnabled",
            name="performance_insights_enabled",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies the Provisioned IOPS (I/O operations per second) value.",  # noqa: E501
            hydrate="PerformanceInsightsRetentionPeriod",
            name="performance_insights_retention_period",
            type=Integer,
        ),
        DataSourceColumn(
            description="If present, specifies the name of the secondary Availability Zone for a DB instance with multi-AZ support.",  # noqa: E501
            hydrate="SecondaryAvailabilityZone",
            name="secondary_availability_zone",
        ),
        DataSourceColumn(
            description="Specifies whether the DB instance is encrypted.",
            hydrate="StorageEncrypted",
            name="storage_encrypted",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies the storage type associated with DB instance.",  # noqa: E501
            hydrate="StorageType",
            name="storage_type",
        ),
        DataSourceColumn(
            description="A list of tags.",
            hydrate="TagList",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_db_instances",
        # KLUDGE: DocDB and Neptune instances are returned.
        # Filtering them out when calling the API would be brittle
        # as we would need to pass all the accepted engines.
        # Any new engine would be ignored until the filter is updated.
        # It seems safer to ignore them on the client-side for the time being.
        "results_filter": 'DBInstances[?!contains(`["docdb", "neptune"]`, Engine)]',
        "service_name": "rds",
    }
