"""Data source for AWS Elastic Compute Cloud (EC2) Classic Load Balancers (CLB)."""
from typing import Dict, List

from sqlalchemy import DateTime, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_clb")
class AwsEc2ClbDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) Classic Load Balancers (CLB)."""

    columns = [
        DataSourceColumn(
            description="The Availability Zones for the load balancer.",
            hydrate="AvailabilityZones",
            name="availability_zones",
            type=ARRAY(Text),
        ),
        DataSourceColumn(
            description="The date and time the load balancer was created.",
            hydrate="CreatedTime",
            name="created_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The IDs of the instances for the load balancer.",
            hydrate="Instances",
            name="instances",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The name of the load balancer.",
            hydrate="LoadBalancerName",
            name="name",
        ),
        DataSourceColumn(
            description="The IDs of the subnets for the load balancer.",
            hydrate="Subnets",
            name="subnet_ids",
            type=ARRAY(Text),
        ),
        DataSourceColumn(
            description="Any tags assigned to the load balancer.",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The ID of the VPC for the load balancer.",
            hydrate="VPCId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "describe_tags",
            "method_parameters": {"LoadBalancerNames": ["{LoadBalancerName}"]},
            "results_filter": '[{"Tags": @.TagDescriptions[0].Tags}]',
            "service_name": "elb",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_load_balancers",
        "results_filter": "LoadBalancerDescriptions[]",
        "service_name": "elb",
    }
