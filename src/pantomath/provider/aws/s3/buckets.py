"""Data source for AWS AWS Simple Storage Service (S3) buckets."""
from sqlalchemy.dialects.postgresql import JSONB

from pantomath.datasource import DataSourceColumn
from pantomath.provider.aws import AwsDataSource, beautify_tags, data_sources


@data_sources.register("aws_s3_buckets")
class AwsS3BucketsDataSource(AwsDataSource):
    """Data source for AWS AWS Simple Storage Service (S3) buckets."""

    columns = [
        DataSourceColumn(
            description="The name of the bucket.",
            hydrate="resource.Name",
            name="name",
        ),
        DataSourceColumn(
            description="The AWS region.",
            hydrate="location.LocationConstraint",
            index=True,
            name="region",
        ),
        DataSourceColumn(
            description="Any tags assigned to the bucket.",
            hydrate="tags.TagSet",
            index=True,
            name="tags",
            transform=beautify_tags,
            type=JSONB,
        ),
        DataSourceColumn(
            description="The versioning state of the bucket.",
            hydrate="versioning.Status",
            name="versioning",
        ),
    ]

    enrich_config = {
        "location": {
            "method_name": "get_bucket_location",
            "method_parameters": {"Bucket": "{Name}"},
            # No value means us-east-1 region
            "results_filter": '[{"LocationConstraint": @.LocationConstraint || `us-east-1`}]',  # noqa: E501
            "service_name": "s3",
        },
        "tags": {
            "method_name": "get_bucket_tagging",
            "method_parameters": {"Bucket": "{Name}"},
            "results_filter": '[{"TagSet": @.TagSet}]',
            "service_name": "s3",
            "expected_errors": ["NoSuchTagSet"],
        },
        "versioning": {
            "method_name": "get_bucket_versioning",
            "method_parameters": {"Bucket": "{Name}"},
            "results_filter": '[{"Status": @.Status}]',
            "service_name": "s3",
        },
    }

    # The region is overridden due to a quirk in how the AWS API works for S3
    excluded_default_columns = ["region"]

    extract_config = {
        "method_name": "list_buckets",
        "results_filter": 'Buckets[].{"Name": @.Name}',
        "service_name": "s3",
    }
