"""Data source for AWS Elastic Compute Cloud (EC2) VPC Endpoints."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_vpc_endpoints")
class AwsEc2VpcEndpointsDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) VPC Endpoints."""

    columns = [
        DataSourceColumn(
            description="The date and time that the VPC endpoint was created.",
            hydrate="CreationTimestamp",
            name="creation_timestamp",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The name of the service to which the endpoint is associated.",
            hydrate="ServiceName",
            name="service_name",
        ),
        DataSourceColumn(
            description="The state of the VPC endpoint.",
            hydrate="State",
            name="state",
            type=ENUM(
                "available",
                "deleted",
                "deleting",
                "expired",
                "failed",
                "pending",
                "pending_acceptance",
                "rejected",
                name="aws_ec2_vpc_endpoints_state_enum",
            ),
        ),
        DataSourceColumn(
            description="Any tags assigned to the VPC endpoint.",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The ID of the VPC endpoint.",
            hydrate="VpcEndpointId",
            name="vpc_endpoint_id",
        ),
        DataSourceColumn(
            description="The type of endpoint.",
            hydrate="VpcEndpointType",
            name="type",
            type=ENUM(
                "Gateway",
                "GatewayLoadBalancer",
                "Interface",
                name="aws_ec2_vpc_endpoints_type_enum",
            ),
        ),
        DataSourceColumn(
            description="The ID of the VPC to which the endpoint is associated.",
            hydrate="VpcId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_vpc_endpoints",
        "results_filter": "VpcEndpoints[]",
        "service_name": "ec2",
    }
