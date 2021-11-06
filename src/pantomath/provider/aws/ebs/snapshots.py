"""Data source for AWS Elastic Block Storage (EBS) snapshots."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_ebs_snapshots")
class AwsEbsSnapshotsDataSource(AwsDataSource):
    """Data source for AWS Elastic Block Storage (EBS) snapshots."""

    columns = [
        DataSourceColumn(
            description="The description for the snapshot",
            hydrate="Description",
            name="description",
        ),
        DataSourceColumn(
            description="Indicates whether the snapshot is encrypted",
            hydrate="Encrypted",
            name="encrypted",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The name the snapshot",
            hydrate="Tags[?Key=='Name'] | [0].Value",
            name="name",
        ),
        DataSourceColumn(
            description="The snapshot ID",
            hydrate="SnapshotId",
            index=True,
            name="snapshot_id",
        ),
        DataSourceColumn(
            description="The time stamp when the snapshot was initiated",
            hydrate="StartTime",
            name="start_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The snapshot state",
            hydrate="State",
            name="state",
            type=ENUM(
                "completed",
                "error",
                "pending",
                name="aws_ebs_snapshots_state_enum",
            ),
        ),
        DataSourceColumn(
            description="The error state details, if applicable",
            hydrate="StateMessage",
            name="state_message",
        ),
        DataSourceColumn(
            description="Any tags assigned to the snapshot",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The volume ID",
            hydrate="VolumeId",
            index=True,
            name="volume_id",
        ),
        DataSourceColumn(
            description="The size of the volume, in GiB",
            hydrate="VolumeSize",
            name="volume_size",
            type=Integer,
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_snapshots",
        # Only the snapshots for this account
        "method_parameters": {"OwnerIds": ["self"]},
        "results_filter": "Snapshots[]",
        "service_name": "ec2",
    }
