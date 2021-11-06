"""Data source for AWS Elastic Container Service (ECS) clusters."""
from typing import Dict, List

from sqlalchemy import Integer
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_ecs_clusters")
class AwsEcsClustersDataSource(AwsDataSource):
    """Data source for AWS Elastic Container Service (ECS) clusters."""

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) that identifies the cluster.",  # noqa: E501
            hydrate="resource.clusterArn",
            name="arn",
        ),
        DataSourceColumn(
            description="A user-generated string that you use to identify your cluster.",  # noqa: E501
            hydrate="cluster.clusterName",
            name="name",
        ),
        DataSourceColumn(
            description="The status of the cluster.",
            hydrate="cluster.status",
            name="status",
            type=ENUM(
                "ACTIVE",
                "DEPROVISIONING",
                "FAILED",
                "INACTIVE",
                "PROVISIONING",
                name="aws_ecs_clusters_status_enum",
            ),
        ),
        DataSourceColumn(
            description="The number of container instances registered into the cluster. This includes container instances in both ACTIVE and DRAINING status.",  # noqa: E501
            hydrate="cluster.registeredContainerInstancesCount",
            name="container_instances_count",
            type=Integer,
        ),
        DataSourceColumn(
            description="The number of tasks in the cluster that are in the RUNNING state.",  # noqa: E501
            hydrate="cluster.runningTasksCount",
            name="running_tasks_count",
            type=Integer,
        ),
        DataSourceColumn(
            description="The number of tasks in the cluster that are in the PENDING state.",  # noqa: E501
            hydrate="cluster.pendingTasksCount",
            name="pending_tasks_count",
            type=Integer,
        ),
        DataSourceColumn(
            description="The number of services that are running on the cluster in an ACTIVE state.",  # noqa: E501
            hydrate="cluster.activeServicesCount",
            name="active_services_count",
            type=Integer,
        ),
        DataSourceColumn(
            description="Any tags assigned to the cluster",
            hydrate="cluster.tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "cluster": {
            "method_name": "describe_clusters",
            "method_parameters": {
                "clusters": ["{clusterArn}"],
                "include": ["TAGS"],
            },
            "results_filter": "clusters[]",
            "service_name": "ecs",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_clusters",
        "results_filter": 'clusterArns[].{"clusterArn": @}',
        "service_name": "ecs",
    }
