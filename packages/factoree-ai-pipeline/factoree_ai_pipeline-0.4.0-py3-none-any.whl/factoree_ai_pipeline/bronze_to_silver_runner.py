import os
import sys
from logging import Logger
from abc import ABC
from typing import final, TypeVar, Generic
from factoree_ai_pipeline.s3.s3_client_utils import get_bronze_bucket_name, get_silver_bucket_name
from factoree_ai_pipeline.s3.s3_utility import S3Utility
from factoree_ai_pipeline.system_params import PATH_SEPARATOR_CHAR, FAILED, INPUT
from factoree_ai_pipeline.file.file_types import S3CsvFile, S3JsonFile, S3FileCreatedEvent, S3File
from factoree_ai_pipeline.transform.transform_utility import TransformUtility

FILE_TYPE = TypeVar('FILE_TYPE', bound=S3File)


class TransformException(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(message)


class BronzeToSilverRunner(ABC, Generic[FILE_TYPE]):
    def __init__(
            self,
            s3_utility: S3Utility,
            transform_utility: TransformUtility,
            environment,
            company,
            site,
            timezone_name,
            logger: Logger,
            is_test: bool = False
    ):
        self.timezone_name = timezone_name
        self.transform_utility = transform_utility
        self.logger = logger
        self.s3_utility = s3_utility
        self.is_test = is_test

        self.bronze_bucket_name = get_bronze_bucket_name(
            environment,
            company,
            site
        )
        self.silver_bucket_name = get_silver_bucket_name(
            environment,
            company,
            site
        )
        self.written_files: list[S3JsonFile] = []

    @final
    def run(self) -> (int, list[S3JsonFile]):
        silver_files: list[S3JsonFile] = []
        silver_files_number: int = 0
        queue_empty = False

        while not queue_empty:
            written_files, queue_empty = self.run_iteration()
            silver_files_number += len(written_files)
            if self.is_test:
                silver_files += written_files

        return silver_files_number, silver_files

    @final
    def run_iteration(self) -> (list[S3JsonFile], bool):
        try:
            file_created_event: S3FileCreatedEvent = self.next_created_file_event()
            return self.attempt_to_run_iteration(file_created_event)
        except Exception as e:
            self.logger.error(f'{str(e)}')
            self.logger.error(f'{sys.exc_info()}')
            return [], False

    @final
    def attempt_to_run_iteration(self, file_created_event: S3FileCreatedEvent) -> (list[S3JsonFile], bool):
        if file_created_event:
            file: FILE_TYPE = self.read_s3_file(file_created_event)
            lines_num = len(file.data)
            self.logger.info(f'Transforming {lines_num} lines of {file.filename}')
            written_silver_files: list[S3JsonFile] = self.transform_bronze_file(file_created_event, file)
            self.move_file_to_completed_folder(file_created_event)
            self.mark_message_as_done(file_created_event)
            queue_empty = False
        else:
            written_silver_files: list[S3JsonFile] = []
            self.logger.info('No files created, exiting.')
            queue_empty = True

        return written_silver_files, queue_empty

    @ final
    def transform_bronze_file(self, event: S3FileCreatedEvent, file_created: FILE_TYPE) -> list[S3JsonFile]:
        silver_files: list[S3JsonFile] = []
        try:
            silver_files, errors = self.transform_utility.transform(
                file_created.bucket_name,
                file_created.data,
                self.timezone_name
            )
            self.logger.info(f'Writing {len(silver_files)} JSON files into {self.silver_bucket_name}')

            self.s3_utility.write_json_files(
                silver_files,
                self.silver_bucket_name
            )

            if len(errors):
                destination_folder = f'{self.bronze_bucket_name}{PATH_SEPARATOR_CHAR}{FAILED}'
                self.logger.warning(f'Writing {len(errors[0])} failed tags into {destination_folder}')
                self.s3_utility.write_csv_file(
                    S3CsvFile(
                        file_created.bucket_name,
                        file_created.filename.replace(INPUT, FAILED),
                        errors
                    ),
                    self.bronze_bucket_name
                )

        except TransformException:
            self.logger.error(f'Error when transforming the data:\n{sys.exc_info()}')
            self.handle_error(
                event,
                file_created
            )

        return silver_files

    @final
    def read_s3_file(self, event: S3FileCreatedEvent) -> FILE_TYPE:
        return self.s3_utility.read_s3_file(event)

    @final
    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        return self.s3_utility.next_created_file_event()

    @final
    def move_file_to_completed_folder(self, file_created_event: S3FileCreatedEvent) -> bool:
        return self.s3_utility.move_file_to_completed_folder(file_created_event)

    @final
    def mark_message_as_done(self, file_created_event: S3FileCreatedEvent) -> bool:
        return self.s3_utility.mark_file_as_done(file_created_event)

    @final
    def move_file_to_failed_folder(self, file_created_event: S3FileCreatedEvent) -> bool:
        return self.s3_utility.move_file_to_failed_folder(file_created_event)

    @final
    def handle_error(self, event: S3FileCreatedEvent, created_file: S3CsvFile):
        failed_file: S3CsvFile = S3CsvFile(
            event.bucket_name,
            os.path.join(FAILED, event.filename),
            created_file.data,
        )
        # TODO: refactor to work on any S3File after refactoring S3Utility into abstract
        self.s3_utility.write_csv_file(failed_file, event.bucket_name)
        self.s3_utility.mark_file_as_done(event)
