from factoree_ai_pipeline.system_params import SEPARATOR_CHAR, COMPONENT_ETL, SUB_COMPONENT_BRONZE, SUB_COMPONENT_SILVER


def get_bronze_bucket_name(environment: str, company: str, site: str) -> str:
    return SEPARATOR_CHAR.join([
        environment,
        COMPONENT_ETL,
        SUB_COMPONENT_BRONZE,
        company,
        site
    ])


def get_silver_bucket_name(environment: str, company: str, site: str) -> str:
    return SEPARATOR_CHAR.join([
        environment,
        COMPONENT_ETL,
        SUB_COMPONENT_SILVER,
        company,
        site
    ])
