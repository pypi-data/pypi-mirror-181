import boto3
import json
from factoree_ai_pipeline.file.file_types import S3TextFile, S3FileCreatedEvent
from logging import Logger


class TestEventError(Exception):
    def __init__(self, handler: str, bucket: str):
        super().__init__('s3:TestEvent received')
        self.handler = handler
        self.bucket = bucket

    def get_handler(self) -> str:
        return self.handler

    def get_bucket(self) -> str:
        return self.bucket


class S3SourceConnector:
    event_list: list[S3FileCreatedEvent] = []
    current_file = None

    def __init__(
            self,
            region_name: str,
            sqs_url: str,
            aws_access_key: str,
            aws_secret_key: str,
            logger: Logger
    ):
        self.sqs_url = sqs_url
        self.aws_access_key = aws_access_key
        self.aws_secret_key = aws_secret_key

        self.sqs_client = boto3.client(
            'sqs',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.s3_client = boto3.client(
            's3',
            aws_access_key_id=self.aws_access_key,
            aws_secret_access_key=self.aws_secret_key,
            region_name=region_name
        )
        self.logger = logger

    def next_created_file_event(self) -> S3FileCreatedEvent | None:
        # TODO: error handling
        self.logger.info(f'Getting events from {self.sqs_url}')
        response = self.sqs_client.receive_message(
            QueueUrl=self.sqs_url,
            MaxNumberOfMessages=1,
        )
        event: S3FileCreatedEvent = S3SourceConnector.get_file_created_event_from_response(response, self.logger)
        if event is None:
            self.logger.info('No messages in queue')
        else:
            self.logger.info(f'Received message of new file {event.filename}')

        return event

    @staticmethod
    def get_file_created_event_from_response(response, logger: Logger) -> S3FileCreatedEvent | None:
        event: S3FileCreatedEvent | None = None
        for message in response.get('Messages', []):
            handler = message.get('ReceiptHandle', '')
            try:
                body_str = message.get('Body')
                body_json = json.loads(body_str)
                if body_json.get('Event') == 's3:TestEvent':
                    raise TestEventError(handler, body_json.get('Bucket'))
                for record in body_json.get('Records', []):
                    filename = record.get('s3', {}).get('object', {}).get('key')
                    bucket_name = record.get('s3', {}).get('bucket', {}).get('name')
                    event = S3FileCreatedEvent(bucket_name, filename, handler)
            except IndexError or TypeError as e:
                logger.error(str(e))

        return event

    def fetch_s3_file(self, bucket_name: str, file_key: str) -> S3TextFile:
        data: str = self.__read_file_content_from_s3(bucket_name, file_key)
        return S3TextFile(bucket_name, file_key, data)

    def purge_events(self):
        self.sqs_client.purge_queue(QueueUrl=self.sqs_url)

    def __read_file_content_from_s3(self, bucket_name: str, s3_path: str) -> str:
        data = self.s3_client.get_object(Bucket=bucket_name, Key=s3_path)
        return data['Body'].read().decode('UTF-8')

    def delete_message(self, handler: str) -> bool:
        # TODO: error handling
        self.logger.info(f'Deleting message with ReceiptHandle "{handler}" from queue')
        self.sqs_client.delete_message(
            QueueUrl=self.sqs_url,
            ReceiptHandle=handler
        )
        return True
