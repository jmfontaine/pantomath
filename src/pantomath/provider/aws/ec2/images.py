"""Data source for AWS Elastic Compute Cloud (EC2) images (AMI)."""
from typing import Dict, List

import dateutil
from sqlalchemy import Boolean, DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_ec2_images")
class AwsEc2ImagesDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) images (AMI)."""

    columns = [
        DataSourceColumn(
            description="The architecture of the image.",
            hydrate="Architecture",
            name="architecture",
            type=ENUM(
                "arm64",
                "i386",
                "x86_64",
                "x86_64_mac",
                name="aws_ec2_images_architecture_enum",
            ),
        ),
        DataSourceColumn(
            description="Any block device mapping entries.",
            hydrate="BlockDeviceMappings",
            name="block_device_mappings",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The date and time the image was created.",
            hydrate="CreationDate",
            name="creation_date",
            transform=dateutil.parser.parse,
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The date and time to deprecate the AMI, in UTC, in the following format: YYYY -MM -DD T*HH* :MM :SS Z.",  # noqa: E501
            hydrate="DeprecationTime",
            name="deprecation_time",
            transform=dateutil.parser.parse,
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The ID of the AMI.",
            hydrate="ImageId",
            index=True,
            name="image_id",
        ),
        DataSourceColumn(
            description="The location of the AMI.",
            hydrate="ImageLocation",
            name="image_location",
        ),
        DataSourceColumn(
            description="The Amazon Web Services account alias (for example, amazon , self ) or the Amazon Web Services account ID of the AMI owner.",  # noqa: E501
            hydrate="ImageOwnerAlias",
            name="image_owner_alias",
        ),
        DataSourceColumn(
            description="The type of the AMI.",
            hydrate="ImageType",
            name="image_type",
            type=ENUM(
                "kernel",
                "machine",
                "ramdisk",
                name="aws_ec2_images_type_enum",
            ),
        ),
        DataSourceColumn(
            description="The name of the AMI that was provided during image creation.",  # noqa: E501
            hydrate="Name",
            name="name",
        ),
        DataSourceColumn(
            description="The ID of the Amazon Web Services account that owns the image.",  # noqa: E501
            hydrate="OwnerId",
            name="owner_id",
        ),
        DataSourceColumn(
            description="This value is set to windows for Windows AMIs; otherwise, it is blank.",  # noqa: E501
            hydrate="Platform",
            name="platform",
        ),
        DataSourceColumn(
            description="Indicates whether the image has public launch permissions. The value is true if this image has public launch permissions or false if it has only implicit and explicit launch permissions.",  # noqa: E501
            hydrate="Public",
            name="public",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Any product codes associated with the AMI.",
            hydrate="ProductCodes",
            name="product_codes",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The current state of the AMI. If the state is available , the image is successfully registered and can be used to launch an instance.",  # noqa: E501
            hydrate="State",
            name="state",
            type=ENUM(
                "available",
                "deregistered",
                "error",
                "failed",
                "invalid",
                "pending",
                "transient",
                name="aws_ec2_images_state_enum",
            ),
        ),
        DataSourceColumn(
            description="The operation of the Amazon EC2 instance and the billing code that is associated with the AMI.",  # noqa: E501
            hydrate="UsageOperation",
            name="usage_operation",
        ),
        DataSourceColumn(
            description="The description of the AMI that was provided during image creation.",  # noqa: E501
            hydrate="Description",
            name="description",
        ),
        DataSourceColumn(
            description="Specifies whether enhanced networking with ENA is enabled.",  # noqa: E501
            hydrate="EnaSupport",
            name="ena_support",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The hypervisor type of the image.",
            hydrate="Hypervisor",
            name="hypervisor",
            type=ENUM("ovm", "xen", name="aws_ec2_images_hypervisor_enum"),
        ),
        DataSourceColumn(
            description="The type of root device used by the AMI. The AMI can use an Amazon EBS volume or an instance store volume.",  # noqa: E501
            hydrate="RootDeviceType",
            name="root_device_type",
            type=ENUM(
                "ebs",
                "instance-store",
                name="aws_ec2_images_root_device_type_enum",
            ),
        ),
        DataSourceColumn(
            description="The message for the reason of the state change.",
            hydrate="StateReason.Message",
            name="state_reason_message",
        ),
        DataSourceColumn(
            description="Any tags assigned to the image.",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The type of virtualization of the AMI.",
            hydrate="VirtualizationType",
            name="virtualization_type",
            type=ENUM(
                "hvm",
                "paravirtual",
                name="aws_ec2_images_virtualization_type_enum",
            ),
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_images",
        "method_parameters": {"Owners": ["self"]},
        "results_filter": "Images[]",
        "service_name": "ec2",
    }
