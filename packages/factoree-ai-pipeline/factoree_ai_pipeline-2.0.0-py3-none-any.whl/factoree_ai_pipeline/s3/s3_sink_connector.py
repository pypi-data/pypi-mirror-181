import json
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import TypeVar
from logging import Logger

from factoree_ai_pipeline.file.file_types import S3File
from factoree_ai_pipeline.file.file_utils import grid_to_csv
from factoree_ai_pipeline.s3.s3_client import S3Client


T = TypeVar('T', bound=S3File)


class S3SinkConnector:
    def __init__(
            self,
            s3_client: S3Client,
            logger: Logger
    ):
        super().__init__()
        self.s3_client = s3_client
        self.logger = logger

    def write_csv_file(self, bucket_name: str, filename: str, data: list[list]) -> bool:
        return self.s3_client.put(bucket_name, filename, grid_to_csv(data))

    def write_json_file(self, bucket_name: str, filename: str, json_data: dict) -> bool:
        self.logger.info(f'write_json_file({filename})')
        return self.s3_client.put(bucket_name, filename, json.dumps(json_data))

    def write_json_files(self, bucket_name: str, filenames: list[str],
                         json_data: list[dict]) -> int:
        max_workers = max(30, len(filenames))
        written_json_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(write_json_file, self, bucket_name, filenames[i], json_data[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                written_json_files += 1 if future.result() else 0

        return written_json_files

    def delete(self, bucket_name: str, filename: str) -> bool:
        return self.s3_client.delete(bucket_name, filename)

    def delete_files(self, bucket_name: str, filenames: list[str]) -> int:
        max_workers = max(30, len(filenames))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, bucket_name, filenames[i]) for i in
                       range(len(filenames))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def delete_s3_files(self, files: list[T]) -> int:
        max_workers = max(30, len(files))
        deleted_files = 0

        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = [executor.submit(delete, self, files[i].bucket_name, files[i].filename) for i in
                       range(len(files))]
            for future in as_completed(futures):
                deleted_files += 1 if future.result() else 0

        return deleted_files

    def copy(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        copy_source = {'Bucket': src_bucket, 'Key': src_filename}
        return self.s3_client.copy(copy_source, dst_bucket, dst_filename)

    def move(self, src_bucket: str, src_filename: str, dst_bucket: str, dst_filename: str) -> bool:
        return self.copy(src_bucket, src_filename, dst_bucket, dst_filename) and self.delete(src_bucket, src_filename)

    def key_exists(self, bucket_name: str, filename: str) -> bool:
        return self.s3_client.key_exists(bucket_name, filename)


def write_json_file(connector: S3SinkConnector, bucket_name: str, filename: str, json_data: dict) -> bool:
    return connector.write_json_file(bucket_name, filename, json_data)


def delete(connector: S3SinkConnector, bucket_name: str, filename: str) -> bool:
    return connector.delete(bucket_name, filename)
