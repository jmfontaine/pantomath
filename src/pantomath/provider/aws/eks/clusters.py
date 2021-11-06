"""Data source for AWS Elastic Kubernetes Service clusters."""
from typing import Dict, List

from sqlalchemy import DateTime
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.provider.aws import AwsDataSource, DataSourceColumn, data_sources


@data_sources.register("aws_eks_clusters")
class AwsEksClustersDataSource(AwsDataSource):
    """Data source for AWS Elastic Kubernetes Service clusters."""

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) of the cluster.",
            hydrate="cluster.arn",
            name="arn",
        ),
        DataSourceColumn(
            description="The Unix epoch timestamp in seconds for when the cluster was created.",  # noqa: E501
            hydrate="cluster.createdAt",
            name="created_at",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The name of the cluster.",
            hydrate="cluster.name",
            name="name",
        ),
        DataSourceColumn(
            description="Any tags assigned to the cluster",
            hydrate="cluster.resourcesVpcConfig",
            name="resources_vpc_config",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The current status of the cluster.",
            hydrate="cluster.status",
            name="status",
        ),
        DataSourceColumn(
            description="Any tags assigned to the cluster",
            hydrate="cluster.tags",
            index=True,
            name="tags",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The Kubernetes server version for the cluster.",
            hydrate="cluster.version",
            name="version",
        ),
    ]

    enrich_config: Dict = {
        "cluster": {
            "method_name": "describe_cluster",
            "method_parameters": {"name": "{Name}"},
            "results_filter": "[cluster]",
            "service_name": "eks",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_clusters",
        "results_filter": 'clusters[].{"Name": @}',
        "service_name": "eks",
    }
