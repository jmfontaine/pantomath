"""Data source for AWS Route53 domains."""
from typing import Dict, List

from sqlalchemy import Boolean, DateTime

from pantomath.provider.aws import AwsDataSource, DataSourceColumn, data_sources


@data_sources.register("aws_route53_domains")
class AwsRoute53DomainsDataSource(AwsDataSource):
    """Data source for AWS Route53 domains."""

    columns = [
        DataSourceColumn(
            description="Indicates whether the domain is automatically renewed upon expiration.",  # noqa: E501
            hydrate="AutoRenew",
            name="auto_renew",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The name of the domain that the summary information applies to.",  # noqa: E501
            hydrate="DomainName",
            name="domain_name",
        ),
        DataSourceColumn(
            description="Expiration date of the domain in Unix time format and Coordinated Universal Time (UTC).",  # noqa: E501
            hydrate="Expiry",
            name="expiry",
            type=DateTime(timezone=True),
        ),
        DataSourceColumn(
            description="Indicates whether a domain is locked from unauthorized transfer to another party.",  # noqa: E501
            hydrate="TransferLock",
            name="transfer_lock",
            type=Boolean,
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "list_domains",
        "results_filter": "Domains[]",
        "service_name": "route53domains",
    }
