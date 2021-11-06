"""Data source for AWS Elastic Compute Cloud (EC2) Application Load Balancers (ALB)."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_ec2_alb")
class AwsEc2AlbDataSource(AwsDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) Application Load Balancers (ALB)."""  # noqa: E501

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) of the load balancer.",
            hydrate="LoadBalancerArn",
            name="arn",
        ),
        DataSourceColumn(
            description="The subnets for the load balancer.",
            hydrate="AvailabilityZones",
            name="availability_zones",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The date and time the load balancer was created.",
            hydrate="CreatedTime",
            name="created_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The name of the load balancer.",
            hydrate="LoadBalancerName",
            name="name",
        ),
        DataSourceColumn(
            description="The state of the load balancer.",
            hydrate="State.Code",
            name="state",
        ),
        DataSourceColumn(
            description="The reason for the state of the load balancer.",
            hydrate="State.Reason",
            name="state_reason",
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
            hydrate="VpcId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "describe_tags",
            "method_parameters": {"ResourceArns": ["{LoadBalancerArn}"]},
            "results_filter": '[{"Tags": @.TagDescriptions[0].Tags}]',
            "service_name": "elbv2",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_load_balancers",
        "results_filter": "LoadBalancers[?Type == 'application']",
        "service_name": "elbv2",
    }
