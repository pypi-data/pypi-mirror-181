from typing import TypeVar, Generic
from factoree_ai_pipeline.file.file_types import S3FileCreatedEvent, S3File, S3TextFile
from factoree_ai_pipeline.s3.s3_source_connector import S3SourceConnector
from factoree_ai_pipeline.text.text_parsers import TextParser

T = TypeVar('T', bound='S3File')


class FormattedS3SourceConnector(Generic[T]):
    def __init__(
        self,
        connector: S3SourceConnector,
        parser: TextParser
    ):
        super().__init__()
        self.connector = connector
        self.parser = parser

    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        return self.connector.next_created_file_event()

    def fetch_s3_file(self, event: S3FileCreatedEvent) -> T:
        bucket_name = event.bucket_name
        file_key = event.filename
        text_file: S3TextFile = self.connector.fetch_s3_file(
            bucket_name,
            file_key
        )
        return S3File[T](bucket_name, file_key, self.parser.parse(text_file.data))

    def mark_file_as_done(self, msg_id: str) -> bool:
        return self.connector.delete_message(msg_id)

    def purge_events(self):
        self.connector.purge_events()
