"""Data source for AWS DocumentDB clusters."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime, Integer, Text
from sqlalchemy.dialects.postgresql import ARRAY, JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_docdb_clusters")
class AwsDocDbClustersDataSource(AwsDataSource):
    """Data source for AWS DocumentDB clusters."""

    columns = [
        DataSourceColumn(
            description="The Amazon Resource Name (ARN) for the cluster.",
            hydrate="DBClusterArn",
            name="arn",
        ),
        DataSourceColumn(
            description="Provides the list of Amazon EC2 Availability Zones that instances in the cluster can be created in.",  # noqa: E501
            hydrate="AvailabilityZones",
            name="availability_zones",
            type=ARRAY(Text),
        ),
        DataSourceColumn(
            description="Specifies the number of days for which automatic snapshots are retained.",  # noqa: E501
            hydrate="BackupRetentionPeriod",
            name="backup_retention_period",
            type=Integer,
        ),
        DataSourceColumn(
            description="A list of log types that this cluster is configured to export to Amazon CloudWatch Logs.",  # noqa: E501
            hydrate="EnabledCloudwatchLogsExports",
            name="cloudwatch_logs_exports",
            type=ARRAY(Text),
        ),
        DataSourceColumn(
            description="Specifies the time when the cluster was created, in Universal Coordinated Time (UTC).",  # noqa: E501
            hydrate="ClusterCreateTime",
            name="cluster_create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Provides the name of the database engine to be used for this cluster.",  # noqa: E501
            hydrate="Engine",
            name="engine",
        ),
        DataSourceColumn(
            description="Indicates the database engine version.",
            hydrate="EngineVersion",
            name="engine_version",
        ),
        DataSourceColumn(
            description="The Region-unique, immutable identifier for the cluster.",
            hydrate="DbClusterResourceId",
            name="id",
        ),
        DataSourceColumn(
            description="Provides the list of instances that make up the cluster.",
            hydrate="DBClusterMembers",
            name="members",
            type=JSONB,
        ),
        DataSourceColumn(
            description="Specifies whether the cluster has instances in multiple Availability Zones.",  # noqa: E501
            hydrate="MultiAZ",
            name="multi_az",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Contains a user-supplied cluster identifier. This identifier is the unique key that identifies a cluster.",  # noqa: E501
            hydrate="DBClusterIdentifier",
            name="name",
        ),
        DataSourceColumn(
            description="Specifies the current state of this cluster.",
            hydrate="Status",
            name="status",
        ),
        DataSourceColumn(
            description="The tags currently associated with the cluster.",
            hydrate="tags.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "tags": {
            "method_name": "list_tags_for_resource",
            "method_parameters": {"ResourceName": "{DBClusterArn}"},
            "results_filter": '[{"Tags": @.TagList}]',
            "service_name": "docdb",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_db_clusters",
        # KLUDGE: Could not make the server-side filter work
        # so filtering on the client side.
        "results_filter": "DBClusters[?Engine=='docdb']",
        "service_name": "docdb",
    }
