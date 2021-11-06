"""Data source for AWS Elastic Compute Cloud (EC2) Gateway Load Balancers (GLB)."""
from typing import Dict

from pantomath.provider.aws import data_sources
from pantomath.provider.aws.ec2.alb import AwsEc2AlbDataSource


@data_sources.register("aws_ec2_glb")
class AwsEc2GlbDataSource(AwsEc2AlbDataSource):
    """Data source for AWS Elastic Compute Cloud (EC2) Gateway Load Balancers (GLB)."""

    extract_config: Dict = {
        "method_name": "describe_load_balancers",
        "results_filter": "LoadBalancers[?Type == 'gateway']",
        "service_name": "elbv2",
    }
