"""Data source for AWS ElastiCache clusters."""
from typing import Dict, List

from sqlalchemy import DateTime, Integer
from sqlalchemy.dialects.postgresql import ENUM, JSONB

from pantomath.provider.aws import AwsDataSource, DataSourceColumn, data_sources


@data_sources.register("aws_elasticache_clusters")
class AwsElasticacheClustersDataSource(AwsDataSource):
    """Data source for AWS ElastiCache clusters."""

    columns = [
        DataSourceColumn(
            description="The ARN of the cache cluster.",
            hydrate="ARN",
            name="arn",
        ),
        DataSourceColumn(
            description="The date and time when the cluster was created.",
            hydrate="CacheClusterCreateTime",
            name="cache_cluster_create_time",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="The user-supplied identifier of the cluster. This identifier is a unique key that identifies a cluster.",  # noqa: E501
            hydrate="CacheClusterId",
            name="cache_cluster_id",
        ),
        DataSourceColumn(
            description="The current state of this cluster.",
            hydrate="CacheClusterStatus",
            name="cache_cluster_status",
            type=ENUM(
                "available",
                "creating",
                "deleted",
                "deleting",
                "incompatible-network",
                "modifying",
                "rebooting cluster nodes",
                "restore-failed",
                "snapshotting",
                name="aws_elasticache_cache_cluster_status_enum",
            ),
        ),
        DataSourceColumn(
            description="The name of the compute and memory capacity node type for the cluster.",  # noqa: E501
            hydrate="CacheNodeType",
            name="cache_node_type",
        ),
        DataSourceColumn(
            description="A list of cache nodes that are members of the cluster.",  # noqa: E501
            hydrate="CacheNodes",
            name="cache_nodes",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The name of the cache engine to be used for this cluster.",  # noqa: E501
            hydrate="Engine",
            name="engine",
            type=ENUM(
                "memcached",
                "redis",
                name="aws_elasticache_engine_enum",
            ),
        ),
        DataSourceColumn(
            description="The version of the cache engine that is used in this cluster.",  # noqa: E501
            hydrate="EngineVersion",
            name="engine_version",
        ),
        DataSourceColumn(
            description="The number of cache nodes in the cluster.",
            hydrate="NumCacheNodes",
            name="num_cache_nodes",
            type=Integer,
        ),
        DataSourceColumn(
            description="The name of the Availability Zone in which the cluster is located or 'Multiple' if the cache nodes are located in different Availability Zones.",  # noqa: E501
            hydrate="PreferredAvailabilityZone",
            name="preferred_availability_zone",
        ),
        DataSourceColumn(
            description="The number of days for which ElastiCache retains automatic cluster snapshots before deleting them.",  # noqa: E501
            hydrate="SnapshotRetentionLimit",
            name="snapshot_retention_limit",
            type=Integer,
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_cache_clusters",
        "results_filter": "CacheClusters[]",
        "service_name": "elasticache",
    }
