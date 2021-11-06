"""Data source for AWS DynamoDB Accelerator (DAX) clusters."""
from typing import Dict, List

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_dax_clusters")
class AwsDaxClustersDataSource(AwsDataSource):
    """Data source for AWS DynamoDB Accelerator (DAX) clusters."""

    columns = [
        DataSourceColumn(
            description="The number of nodes in the cluster that are active.",
            hydrate="ActiveNodes",
            name="active_nodes",
            type=Integer,
        ),
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) that uniquely identifies the cluster.",  # noqa: E501
            hydrate="ClusterArn",
            name="arn",
        ),
        DataSourceColumn(
            description="The name of the DAX cluster.",
            hydrate="ClusterName",
            name="name",
        ),
        DataSourceColumn(
            description="The description of the cluster.",
            hydrate="Description",
            name="description",
        ),
        DataSourceColumn(
            description="The node type for the nodes in the cluster.",
            hydrate="NodeType",
            name="node_type",
        ),
        DataSourceColumn(
            description="The current status of the cluster.",
            hydrate="Status",
            name="status",
        ),
        DataSourceColumn(
            description="The tags currently associated with the DAX cluster.",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The total number of nodes in the cluster.",
            hydrate="TotalNodes",
            name="total_nodes",
            type=Integer,
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "list_tags",
            "method_parameters": {"ResourceName": "{ClusterName}}"},
            "results_filter": "Tags[]",
            "service_name": "dax",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_clusters",
        "results_filter": "Clusters[]",
        "service_name": "dax",
    }
