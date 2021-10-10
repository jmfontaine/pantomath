from typing import Dict

from pantomath.provider.aws import data_sources
from pantomath.provider.aws.ec2.alb import AwsEc2AlbDataSource


@data_sources.register("aws_ec2_nlb")
class AwsEc2NlbDataSource(AwsEc2AlbDataSource):
    extract_config: Dict = {
        "method_name": "describe_load_balancers",
        "results_filter": "LoadBalancers[?Type == 'network']",
        "service_name": "elbv2",
    }
