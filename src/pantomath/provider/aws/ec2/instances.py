"""Data source for AWS Elastic Compute Cloud (EC2) instances."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime
from sqlalchemy.dialects.postgresql import ENUM, INET, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_instances")
class AwsEc2InstancesDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) instances."""

    columns = [
        DataSourceColumn(
            description="The architecture of the image",
            hydrate="Architecture",
            name="architecture",
            type=ENUM(
                "arm64",
                "i386",
                "x86_64",
                name="aws_ec2_instances_architecture_enum",
            ),
        ),
        DataSourceColumn(
            description="Indicates whether the instance is optimized for Amazon EBS I/O",  # noqa: E501
            hydrate="EbsOptimized",
            name="ebs_optimized",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies whether enhanced networking with ENA is enabled",  # noqa: E501
            hydrate="EnaSupport",
            name="ena_support",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The hypervisor type of the instance. The value xen is used for both Xen and Nitro hypervisors",  # noqa: E501
            hydrate="Hypervisor",
            type=ENUM("ovm", "xen", name="aws_ec2_instances_hypervisor_enum"),
            name="hypervisor",
        ),
        DataSourceColumn(
            description="The ID of the AMI used to launch the instance",
            hydrate="ImageId",
            index=True,
            name="image_id",
        ),
        DataSourceColumn(
            description="The ID of the instance",
            hydrate="InstanceId",
            index=True,
            name="instance_id",
        ),
        DataSourceColumn(
            description="Indicates whether this is a Spot Instance or a Scheduled Instance",  # noqa: E501
            hydrate="InstanceLifecycle",
            type=ENUM(
                "scheduled",
                "spot",
                name="aws_ec2_instances_instance_lifecycle_enum",
            ),
            name="instance_lifecycle",
        ),
        DataSourceColumn(
            description="The instance type",
            hydrate="InstanceType",
            name="instance_type",
            index=True,
        ),
        DataSourceColumn(
            description="The name of the key pair, if this instance was launched with an associated key pair",  # noqa: E501
            hydrate="KeyName",
            name="key_name",
        ),
        DataSourceColumn(
            description="The time the instance was launched",
            hydrate="LaunchTime",
            name="launch_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Indicates whether detailed monitoring is enabled. Otherwise, basic monitoring is enabled",  # noqa: E501
            hydrate="Monitoring.State",
            name="monitoring_state",
            type=ENUM(
                "disabled",
                "disabling",
                "enabled",
                "pending",
                name="aws_ec2_instances_monitoring_state_enum",
            ),
        ),
        DataSourceColumn(
            description="The name the instance",
            hydrate="Tags[?Key=='Name'] | [0].Value",
            name="name",
        ),
        DataSourceColumn(
            description="The Availability Zone of the instance",
            hydrate="Placement.AvailabilityZone",
            name="placement_availability_zone",
        ),
        DataSourceColumn(
            description="The tenancy of the instance (if the instance is running in a VPC). An instance with a tenancy of dedicated runs on single-tenant hardware",  # noqa: E501
            hydrate="Placement.Tenancy",
            name="placement_tenancy",
            type=ENUM(
                "default",
                "dedicated",
                "host",
                name="aws_ec2_instances_placement_tenancy_enum",
            ),
        ),
        DataSourceColumn(
            description="The value is Windows for Windows instances; otherwise blank",  # noqa: E501
            hydrate="Platform",
            name="platform",
        ),
        DataSourceColumn(
            description="The private IPv4 address assigned to the instance",
            hydrate="PrivateIpAddress",
            name="private_ip_address",
            type=INET,
        ),
        DataSourceColumn(
            description="The product codes attached to this instance, if applicable",  # noqa: E501
            hydrate="ProductCodes",
            name="product_codes",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The public IPv4 address, or the Carrier IP address assigned to the instance, if applicable",  # noqa: E501
            hydrate="PublicIpAddress",
            name="public_ip_address",
            type=INET,
        ),
        DataSourceColumn(
            description="The ID of the requester that launched the instances on your behalf (for example, Amazon Web Services Management Console or Auto Scaling)",  # noqa: E501
            hydrate="RequesterId",
            name="requester_id",
        ),
        DataSourceColumn(
            description="The current state of the instance",
            hydrate="State.Name",
            index=True,
            name="state_name",
            type=ENUM(
                "pending",
                "running",
                "shutting-down",
                "stopped",
                "stopping",
                "terminated",
                name="aws_ec2_instances_state_name_enum",
            ),
        ),
        DataSourceColumn(
            description="The reason for the most recent state transition. This might be an empty string",  # noqa: E501
            hydrate="StateTransitionReason",
            name="state_transition_reason",
        ),
        DataSourceColumn(
            description="The ID of the subnet in which the instance is running",
            hydrate="SubnetId",
            name="subnet_id",
        ),
        DataSourceColumn(
            description="Any tags assigned to the instance",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The virtualization type of the instance",
            hydrate="VirtualizationType",
            name="virtualization_type",
            type=ENUM(
                "hvm",
                "paravirtual",
                name="aws_ec2_instances_virtualization_type_enum",
            ),
        ),
        DataSourceColumn(
            description="The ID of the VPC in which the instance is running",
            hydrate="VpcId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_instances",
        "results_filter": "Reservations[*].Instances[]",
        "service_name": "ec2",
    }
