"""Data source for AWS Elastic Block Storage (EBS) volumes."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_ebs_volumes")
class AwsEbsVolumesDataSource(AwsDataSource):
    """Data source for AWS Elastic Block Storage (EBS) volumes."""

    columns = [
        DataSourceColumn(
            description="Information about the volume attachments",
            hydrate="Attachments",
            name="attachments",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The Availability Zone for the volume",
            hydrate="AvailabilityZone",
            name="availability_zone",
        ),
        DataSourceColumn(
            description="Indicates whether the volume is encrypted",
            hydrate="CreateTime",
            name="create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Indicates whether the volume is encrypted",
            hydrate="Encrypted",
            name="encrypted",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The number of I/O operations per second (IOPS). For gp3 , io1 , and io2 volumes, this represents the number of IOPS that are provisioned for the volume. For gp2 volumes, this represents the baseline performance of the volume and the rate at which the volume accumulates I/O credits for bursting",  # noqa: E501
            hydrate="Iops",
            name="iops",
            type=Integer,
        ),
        DataSourceColumn(
            description="Indicates whether Amazon EBS Multi-Attach is enabled",
            hydrate="MultiAttachEnabled",
            name="multi_attach_enabled",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The name the volume",
            hydrate="Tags[?Key=='Name'] | [0].Value",
            name="name",
        ),
        DataSourceColumn(
            description="The size of the volume, in GiBs",
            hydrate="Size",
            name="size",
            type=Integer,
        ),
        DataSourceColumn(
            description="The snapshot from which the volume was created, if applicable",  # noqa: E501
            hydrate="SnapshotId",
            name="snapshot_id",
        ),
        DataSourceColumn(
            description="The volume state",
            hydrate="State",
            name="state",
            type=ENUM(
                "available",
                "creating",
                "deleted",
                "deleting",
                "error",
                "in-use",
                name="aws_ebs_volumes_state_enum",
            ),
        ),
        DataSourceColumn(
            description="Any tags assigned to the volume",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            hydrate="Throughput",
            name="throughput",
            type=Integer,
            description="The throughput that the volume supports, in MiB/s",
        ),
        DataSourceColumn(
            description="The ID of the volume",
            hydrate="VolumeId",
            index=True,
            name="volume_id",
        ),
        DataSourceColumn(
            description="The volume type",
            hydrate="VolumeType",
            index=True,
            name="volume_type",
            type=ENUM(
                "gp2",
                "gp3",
                "io1",
                "io2",
                "sc1",
                "st1",
                "standard",
                name="aws_ebs_volumes_volume_type_enum",
            ),
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_volumes",
        "results_filter": "Volumes[]",
        "service_name": "ec2",
    }
