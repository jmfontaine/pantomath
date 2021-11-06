"""Data source for AWS Relational Database Service (RDS) snapshots."""
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


@data_sources.register("aws_rds_snapshots")
class AwsRdsSnapshotsDataSource(AwsDataSource):
    """Data source for AWS Relational Database Service (RDS) snapshots."""

    columns = [
        DataSourceColumn(
            description="Specifies the name of the Availability Zone the DB instance was located in at the time of the DB snapshot.",  # noqa: E501
            hydrate="AvailabilityZone",
            name="availability_zone",
        ),
        DataSourceColumn(
            description="Specifies the allocated storage size in gibibytes (GiB).",  # noqa: E501
            hydrate="AllocatedStorage",
            name="allocated_storage",
            type=Integer,
        ),
        DataSourceColumn(
            description="Specifies the DB instance identifier of the DB instance this DB snapshot was created from.",  # noqa: E501
            hydrate="DBInstanceIdentifier",
            name="db_instance_identifier",
        ),
        DataSourceColumn(
            description="Specifies the identifier for the DB snapshot.",
            hydrate="DBSnapshotIdentifier",
            name="db_snapshot_identifier",
        ),
        DataSourceColumn(
            description="Specifies whether the DB snapshot is encrypted.",
            hydrate="Encrypted",
            name="encrypted",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies the name of the database engine.",
            hydrate="Engine",
            name="engine",
        ),
        DataSourceColumn(
            description="Specifies the version of the database engine.",
            hydrate="EngineVersion",
            name="engine_version",
        ),
        DataSourceColumn(
            description="Specifies the Provisioned IOPS (I/O operations per second) value of the DB instance at the time of the snapshot.",  # noqa: E501
            hydrate="Iops",
            name="iops",
            type=Integer,
        ),
        DataSourceColumn(
            description="License model information for the restored DB instance.",  # noqa: E501
            hydrate="LicenseModel",
            name="license_model",
        ),
        DataSourceColumn(
            description="Specifies the time of the CreateDBSnapshot operation in Coordinated Universal Time (UTC). Doesn't change when the snapshot is copied.",  # noqa: E501
            hydrate="OriginalSnapshotCreateTime",
            name="original_snapshot_create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Specifies when the snapshot was taken in Coordinated Universal Time (UTC). Changes for the copy when the snapshot is copied.",  # noqa: E501
            hydrate="SnapshotCreateTime",
            name="snapshot_create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Provides the type of the DB snapshot.",
            hydrate="SnapshotType",
            name="snapshot_type",
        ),
        DataSourceColumn(
            description="The DB snapshot Amazon Resource Name (ARN) that the DB snapshot was copied from. It only has a value in the case of a cross-account or cross-Region copy.",  # noqa: E501
            hydrate="SourceDBSnapshotIdentifier",
            name="source_db_snapshot_identifier",
        ),
        DataSourceColumn(
            description="The Amazon Web Services Region that the DB snapshot was created in or copied from.",  # noqa: E501
            hydrate="SourceRegion",
            name="source_region",
        ),
        DataSourceColumn(
            description="Specifies the status of this DB snapshot.",
            hydrate="Status",
            name="status",
        ),
        DataSourceColumn(
            description="Specifies the storage type associated with DB snapshot.",  # noqa: E501
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
        "method_name": "describe_db_snapshots",
        "results_filter": "DBSnapshots[]",
        "service_name": "rds",
    }
