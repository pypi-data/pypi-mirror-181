from abc import ABC
from dataclasses import dataclass
from typing import TypeVar, Generic

T = TypeVar('T')


@dataclass
class S3File(ABC, Generic[T]):
    bucket_name: str
    filename: str
    data: T


@dataclass
class S3TextFile(S3File[str]):
    pass


@dataclass
class S3CsvFile(S3File[list[list]]):
    pass


@dataclass
class S3JsonFile(S3File[dict]):
    pass


@dataclass
class S3FileCreatedEvent:
    bucket_name: str
    filename: str
    sqs_msg_id: str
