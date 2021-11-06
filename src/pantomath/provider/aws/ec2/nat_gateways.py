"""Data source for AWS Elastic Compute Cloud (EC2) NAT Gateways."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_nat_gateways")
class AwsEc2NatGatewaysDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) NAT Gateways."""

    columns = [
        DataSourceColumn(
            description="The date and time the NAT gateway was created.",
            hydrate="CreateTime",
            name="create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The date and time the NAT gateway was deleted, if applicable.",
            hydrate="DeleteTime",
            name="delete_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="If the NAT gateway could not be created, specifies the error code for the failure.",  # noqa: E501
            hydrate="FailureCode",
            name="failure_code",
        ),
        DataSourceColumn(
            description="If the NAT gateway could not be created, specifies the error message for the failure, that corresponds to the error code.",  # noqa: E501
            hydrate="FailureMessage",
            name="failure_message",
        ),
        DataSourceColumn(
            description="The ID of the NAT gateway.",
            hydrate="NatGatewayId",
            name="id",
        ),
        DataSourceColumn(
            description="Any tags assigned to the NAT gateway.",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="Information about the IP addresses and network interface associated with the NAT gateway.",  # noqa: E501
            hydrate="NatGatewayAddresses",
            name="nat_gateway_addresses",
            type=JSONB,
        ),
        DataSourceColumn(
            description="Provisioned bandwidth information.",
            hydrate="ProvisionedBandwidth",
            name="provisioned_bandwidth",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The state of the NAT gateway.",
            hydrate="State",
            name="state",
            type=ENUM(
                "available",
                "deleted",
                "deleting",
                "failed",
                "pending",
                name="aws_ec2_nat_gateways_state_enum",
            ),
        ),
        DataSourceColumn(
            description="The ID of the subnet in which the NAT gateway is located.",
            hydrate="SubnetId",
            name="subnet_id",
        ),
        DataSourceColumn(
            description="The ID of the VPC in which the NAT gateway is located.",
            hydrate="VpcId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_nat_gateways",
        "results_filter": "NatGateways[]",
        "service_name": "ec2",
    }
