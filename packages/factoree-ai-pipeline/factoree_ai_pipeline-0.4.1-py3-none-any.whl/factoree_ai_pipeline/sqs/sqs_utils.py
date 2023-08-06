from factoree_ai_pipeline.system_params import SQS_SEPARATOR_CHAR, COMPONENT_ETL, INPUT


def get_sqs_url(
        aws_account_number: str,
        region_name: str,
        environment: str,
        sub_component: str,
        company: str,
        site: str,
        folder: str = INPUT) -> str:
    queue_name = SQS_SEPARATOR_CHAR.join([
        environment,
        COMPONENT_ETL,
        sub_component,
        company,
        site,
        folder,
        'notifications'
    ])
    return f'https://sqs.{region_name}.amazonaws.com/{str(aws_account_number)}/{queue_name}'


def get_multi_bucket_sqs_url(
        aws_account_number: str,
        region_name: str,
        environment: str,
        sub_component: str,
        folder: str = INPUT
) -> str:
    queue_name = SQS_SEPARATOR_CHAR.join([
        environment,
        COMPONENT_ETL,
        sub_component,
        folder,
        'notifications'
    ])
    return f'https://sqs.{region_name}.amazonaws.com/{str(aws_account_number)}/{queue_name}'
