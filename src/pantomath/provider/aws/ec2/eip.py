"""Data source for AWS Elastic Compute Cloud (EC2) Elastic IP Addresses (EIP)."""
from typing import Dict, List

from sqlalchemy.dialects.postgresql import JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_eip")
class AwsEc2EipDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) Elastic IP Addresses (EIP)."""

    columns = [
        DataSourceColumn(
            description="The ID of the instance that the address is associated with (if any).",  # noqa: E501
            hydrate="InstanceId",
            name="instance_id",
        ),
        DataSourceColumn(
            description="The Elastic IP address.",
            hydrate="PublicIp",
            name="public_ip_address",
        ),
        DataSourceColumn(
            description="The Elastic IP address.",
            hydrate="PrivateIpAddress",
            name="private_ip_address",
        ),
        DataSourceColumn(
            description="Any tags assigned to the Elastic IP address.",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_addresses",
        "results_filter": "Addresses[]",
        "service_name": "ec2",
    }
