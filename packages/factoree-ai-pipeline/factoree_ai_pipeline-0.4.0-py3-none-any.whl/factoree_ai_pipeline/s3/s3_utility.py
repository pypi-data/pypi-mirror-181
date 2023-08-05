from time import sleep
from factoree_ai_pipeline.file.file_types import S3FileCreatedEvent, S3CsvFile, S3JsonFile
from factoree_ai_pipeline.s3.s3_sink_connector import S3SinkConnector
from factoree_ai_pipeline.s3.s3_client import S3Client
from factoree_ai_pipeline.system_params import INPUT, FAILED, COMPLETED, PATH_SEPARATOR_CHAR
from factoree_ai_pipeline.s3.formatted_s3_source_connector import FormattedS3SourceConnector
from factoree_ai_pipeline.s3.s3_source_connector import S3SourceConnector
from factoree_ai_pipeline.sqs.sqs_utils import get_sqs_url
from logging import Logger


# TODO: refactor into generic and use of S3CsvUtility sub-class; TypeVar in line 13 not applied?
from factoree_ai_pipeline.text.text_parsers import CsvParser


class S3Utility:
    def __init__(
            self,
            environment: str,
            sub_component: str,
            company: str,
            site: str,
            aws_account: str,
            region_name: str,
            aws_access_key: str,
            aws_secret_key: str,
            datetime_format: str,
            timestamp_column: int,
            logger: Logger
    ):
        self.sqs_url = get_sqs_url(
            aws_account,
            region_name,
            environment,
            sub_component,
            company,
            site,
            INPUT
        )
        self.source_connector: FormattedS3SourceConnector[list[list[any]]] = FormattedS3SourceConnector(
            S3SourceConnector(
                region_name,
                self.sqs_url,
                aws_access_key,
                aws_secret_key,
                logger
            ),
            CsvParser(logger, datetime_format, timestamp_column)
        )
        self.sink_connector = S3SinkConnector(
            S3Client(aws_access_key, aws_secret_key),
            logger
        )
        self.logger = logger

    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        return self.source_connector.next_created_file_event()

    def read_s3_file(self, event: S3FileCreatedEvent) -> S3CsvFile:
        # TODO: refactor to use generic T
        # TODO: rename formatted_s3_source_connector.fetch_s3_file() into read_s3_file() as it fetches and parses
        file: S3CsvFile = self.source_connector.fetch_s3_file(event)
        sleep(2)
        return file

    def write_json_files(self, files: list[S3JsonFile], s3_bucket: str) -> int:
        file_names: list[str] = []
        data: list[dict] = []
        for file in files:
            file_names.append(file.filename)
            data.append(file.data)

        return self.sink_connector.write_json_files(s3_bucket, file_names, data)

    def write_csv_file(self, file: S3CsvFile, s3_bucket: str) -> bool:
        return self.sink_connector.write_csv_file(s3_bucket, file.filename, file.data)

    def mark_file_as_done(self, event: S3FileCreatedEvent):
        self.source_connector.mark_file_as_done(event.sqs_msg_id)

    def move_file_to_completed_folder(self, event: S3FileCreatedEvent) -> bool:
        return self.__move_file(
            event.bucket_name,
            event.filename,
            event.filename.replace(f'{INPUT}{PATH_SEPARATOR_CHAR}', f'{COMPLETED}{PATH_SEPARATOR_CHAR}')
        )

    def move_file_to_failed_folder(self, event: S3FileCreatedEvent) -> bool:
        return self.__move_file(
            event.bucket_name,
            event.filename,
            event.filename.replace(f'{INPUT}{PATH_SEPARATOR_CHAR}', f'{FAILED}{PATH_SEPARATOR_CHAR}')
        )

    def __move_file(self, bucket_name: str, src_filename: str, dst_filename: str) -> bool:
        self.logger.info(f'Moving file from {src_filename} to {dst_filename}')
        return self.sink_connector.move(bucket_name, src_filename, bucket_name, dst_filename)
