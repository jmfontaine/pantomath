"""Data source for AWS CloudTrail trails."""
from typing import Dict, List

from sqlalchemy import Boolean

from pantomath.provider.aws import AwsDataSource, DataSourceColumn, data_sources


@data_sources.register("aws_cloudtrail_trails")
class AwsCloudtrailTrailsDataSource(AwsDataSource):
    """Data source for AWS CloudTrail trails."""

    columns = [
        DataSourceColumn(
            description="The ARN of the trail.",
            hydrate="TrailARN",
            name="arn",
        ),
        DataSourceColumn(
            description="The ARN of the CloudWatch log group to which CloudTrail logs will be delivered.",  # noqa: E501
            hydrate="CloudWatchLogsLogGroupArn",
            name="cloudwatch_logs_log_group_arn",
        ),
        DataSourceColumn(
            description="Specifies if the trail has custom event selectors.",
            hydrate="HasCustomEventSelectors",
            name="has_custom_event_selectors",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies whether a trail has insight types specified in an InsightSelector list.",  # noqa: E501
            hydrate="HasInsightSelectors",
            name="has_insight_selectors",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The region in which the trail was created.",
            hydrate="HomeRegion",
            name="home_region",
        ),
        DataSourceColumn(
            description="Specifies whether the trail exists only in one region or exists in all regions.",  # noqa: E501
            hydrate="IsMultiRegionTrail",
            name="is_multi_region_trail",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies whether the trail is an organization trail.",
            hydrate="IsOrganizationTrail",
            name="is_organization_trail",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Set to True to include Amazon Web Services API calls from Amazon Web Services global services such as IAM. Otherwise, False.",  # noqa: E501
            hydrate="IncludeGlobalServiceEvents",
            name="include_global_service_events",
            type=Boolean,
        ),
        DataSourceColumn(
            description="Specifies whether log file validation is enabled.",
            hydrate="LogFileValidationEnabled",
            name="log_file_validation_enabled",
            type=Boolean,
        ),
        DataSourceColumn(
            description="The name of the trail.",
            hydrate="Name",
            name="name",
        ),
        DataSourceColumn(
            description="Name of the Amazon S3 bucket into which CloudTrail delivers your trail files.",  # noqa: E501
            hydrate="S3BucketName",
            name="s3_bucket_name",
        ),
        DataSourceColumn(
            description="Specifies the Amazon S3 key prefix that comes after the name of the bucket you have designated for log file delivery.",  # noqa: E501
            hydrate="S3KeyPrefix",
            name="s3_key_prefix",
        ),
        DataSourceColumn(
            description="Specifies the ARN of the Amazon SNS topic that CloudTrail uses to send notifications when log files are delivered.",  # noqa: E501
            hydrate="SnsTopicARN",
            name="sns_topic_arn",
        ),
    ]

    enrich_config: Dict = {}

    excluded_default_columns: List[str] = []

    extract_config = {
        "method_name": "describe_trails",
        "results_filter": "trailList[]",
        "service_name": "cloudtrail",
    }
