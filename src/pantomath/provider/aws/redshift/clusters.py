"""Data source for AWS Redshift clusters."""
from typing import Dict, List

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_redshift_clusters")
class AwsRedshiftClustersDataSource(AwsDataSource):
    """Data source for AWS Redshift clusters."""

    columns = [
        DataSourceColumn(
            description="The name of the Availability Zone in which the cluster is located.",  # noqa: E501
            hydrate="AvailabilityZone",
            name="availability_zone",
        ),
        DataSourceColumn(
            description="The unique identifier of the cluster.",
            hydrate="ClusterIdentifier",
            name="cluster_identifier",
        ),
        DataSourceColumn(
            description="The date and time that the cluster was created.",
            hydrate="ClusterCreateTime",
            name="create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The node type for the nodes in the cluster.",
            hydrate="NodeType",
            name="node_type",
        ),
        DataSourceColumn(
            description="The current state of the cluster.",
            hydrate="ClusterStatus",
            name="status",
        ),
        DataSourceColumn(
            description="Any tags assigned to the cluster",
            hydrate="Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The total storage capacity of the cluster in megabytes.",
            hydrate="TotalStorageCapacityInMegaBytes",
            name="total_storage_capacity",
            type=Integer,
        ),
        DataSourceColumn(
            description="The identifier of the VPC the cluster is in, if the cluster is in a VPC.",  # noqa: E501
            hydrate="VpcId",
            name="vpc_id",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_clusters",
        "results_filter": "Clusters[]",
        "service_name": "redshift",
    }
