"""Data source for AWS Elasticsearch Service (ES) domains."""
from typing import Dict, List

from sqlalchemy.dialects.postgresql import JSONB

from pantomath.provider.aws import (
    AwsDataSource,
    DataSourceColumn,
    beautify_tags,
    data_sources,
)


@data_sources.register("aws_es_domains")
class AwsEsDomainsDataSource(AwsDataSource):
    """Data source for AWS Elasticsearch Service (ES) domains."""

    columns = [
        DataSourceColumn(
            description="The Amazon resource name (ARN) of the Elasticsearch domain.",
            hydrate="domain.ARN",
            name="arn",
        ),
        DataSourceColumn(
            description="The type and number of instances in the domain cluster.",
            hydrate="domain.ElasticsearchClusterConfig",
            name="cluster_config",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The EBSOptions for the domain.",
            hydrate="domain.EBSOptions",
            name="ebs_options",
            type=JSONB,
        ),
        DataSourceColumn(
            description="The unique identifier for the specified Elasticsearch domain.",
            hydrate="domain.DomainId",
            name="id",
        ),
        DataSourceColumn(
            description="The name of an Elasticsearch domain.",
            hydrate="domain.DomainName",
            name="name",
        ),
        DataSourceColumn(
            description="Any tags assigned to the cluster",
            hydrate="domain.Tags",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The VPCOptions for the domain.",
            hydrate="domain.VPCOptions",
            name="vpc_options",
            type=JSONB,
        ),
    ]

    enrich_config: Dict = {
        "domain": {
            "method_name": "describe_elasticsearch_domains",
            "method_parameters": {"DomainNames": ["{DomainName}"]},
            "results_filter": "DomainStatusList[]",
            "service_name": "es",
        },
        "tags": {
            "method_name": "list_tags",
            "method_parameters": {
                "ARN": "arn:aws:es:{metadata[region]}:{metadata[account_id]}:domain/{DomainName}"  # noqa: E501
            },
            "results_filter": '[{"Tags": @.TagList}]',
            "service_name": "es",
        },
    }

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_domain_names",
        "results_filter": 'DomainNames[].{"DomainName": @.DomainName}',
        "service_name": "es",
    }
