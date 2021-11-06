"""Data source for AWS Elastic MapReduce (EMR) clusters."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime, Integer
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_emr_clusters")
class AwsEmrClustersDataSource(AwsDataSource):
    """Data source for AWS Elastic MapReduce (EMR) clusters."""

    columns = [
        DataSourceColumn(
            description="The applications installed on this cluster.",
            hydrate="cluster.Applications",
            name="applications",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The Amazon Resource Name of the cluster.",
            hydrate="cluster.ClusterArn",
            name="arn",
        ),
        DataSourceColumn(
            description="Specifies whether the cluster should terminate after completing all steps.",  # noqa: E501
            hydrate="cluster.AutoTerminate",
            name="auto_terminate",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The creation date and time of the cluster.",
            hydrate="cluster.Status.Timeline.CreationDateTime",
            name="creation_date_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The size, in GiB, of the Amazon EBS root device volume of the Linux AMI that is used for each EC2 instance.",  # noqa: E501
            hydrate="cluster.EbsRootVolumeSize",
            name="ebs_root_volume_size",
            type=Integer,
        ),
        DataSourceColumn(
            description="The date and time when the cluster was terminated.",
            hydrate="cluster.Status.Timeline.EndDateTime",
            name="end_date_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The unique identifier for the cluster.",
            hydrate="cluster.Id",
            name="id",
        ),
        DataSourceColumn(
            description="The name of the cluster.",
            hydrate="cluster.Name",
            name="name",
        ),
        DataSourceColumn(
            description="The reason for the cluster status change.",
            hydrate="cluster.NormalizedInstanceHours",
            name="normalized_instance_hours",
            type=Integer,
        ),
        DataSourceColumn(
            description="The date and time when the cluster was ready to run steps.",
            hydrate="cluster.Status.Timeline.ReadyDateTime",
            name="ready_date_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The way that individual Amazon EC2 instances terminate when an automatic scale-in activity occurs or an instance group is resized.",  # noqa: E501
            hydrate="cluster.ScaleDownBehavior",
            name="scale_down_behavior",
        ),
        DataSourceColumn(
            description="The current status of the cluster.",
            hydrate="cluster.Status.State",
            name="status",
        ),
        DataSourceColumn(
            description="The reason for the cluster status change.",
            hydrate="cluster.Status.StateChangeReason.Message",
            name="status_change_reason",
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
            "method_name": "describe_cluster",
            "method_parameters": {"ClusterId": "{Id}"},
            "results_filter": "[Cluster]",
            "service_name": "emr",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_clusters",
        "results_filter": 'Clusters[].{"Id": @.Id}',
        "service_name": "emr",
    }
