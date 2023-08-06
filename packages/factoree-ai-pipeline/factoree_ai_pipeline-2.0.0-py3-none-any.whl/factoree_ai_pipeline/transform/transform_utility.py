from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime, timezone
from typing import Generic, final
from logging import Logger
from typing import TypeVar
from zoneinfo import ZoneInfo
from factoree_ai_pipeline.file.file_types import S3JsonFile
from factoree_ai_pipeline.sensor_type import SensorType, BOOLEAN
from factoree_ai_pipeline.system_params import SUB_COMPONENT_BRONZE, SUB_COMPONENT_SILVER

DATA_TYPE = TypeVar('DATA_TYPE')
TransformOutput = list[S3JsonFile]
TransformTuple = (TransformOutput, DATA_TYPE)
TIME_KEY = 'time'
VALUES_KEY = 'values'
ERRORS_KEY = 'errors'
PHASE_ID_KEY = 'phase_id'
DATA_KEY = 'data'
DATA_TYPE_KEY = 'data_type'
DISCONNECTED_MESSAGE = 'Disconnected'


@dataclass
class TransformationInnerOutput:
    transformed_data_by_sensor_type: dict[SensorType, dict]
    filenames: dict[SensorType, str]


class TransformUtility(ABC, Generic[DATA_TYPE]):
    def __init__(
            self,
            timezone_name: str,
            logger: Logger,
            is_test: bool = False
    ):
        self.zone_info = ZoneInfo(timezone_name)
        self.logger = logger
        self.is_test = is_test

    @final
    def transform(self, bucket_name: str, file_data: DATA_TYPE) -> TransformTuple:
        standardized_data, unprocessed_tags = self.standardize_file_data(file_data)
        output: TransformationInnerOutput = self.transform_data_to_silver_format(standardized_data)
        output_files: list[S3JsonFile] = TransformUtility.construct_output_files(
            bucket_name, output.transformed_data_by_sensor_type, output.filenames
        )
        return output_files, unprocessed_tags

    # noinspection PyMethodMayBeStatic
    def is_data_type_mismatch(self, value: str | float | int | bool | datetime, sensor_type: SensorType) -> bool:
        if isinstance(value, str) and sensor_type.value.get(DATA_TYPE) != BOOLEAN:
            return True
        return False

    @abstractmethod
    def standardize_file_data(self, file_data: DATA_TYPE) -> (DATA_TYPE, DATA_TYPE):
        pass

    @abstractmethod
    def transform_data_to_silver_format(
            self, file_data: DATA_TYPE
    ) -> TransformationInnerOutput:
        pass

    # noinspection PyMethodMayBeStatic
    def standardize_value(
            self, sensor_type: SensorType, value: int | str | float | str | datetime
    ) -> int | str | float | str | datetime:
        if isinstance(value, datetime):
            return datetime(
                value.year, value.month, value.day, value.hour, value.minute, value.second, tzinfo=self.zone_info
            ).astimezone(timezone.utc)

        if sensor_type == SensorType.II and isinstance(value, float) and value < 0.0:
            return DISCONNECTED_MESSAGE
        return value

    @staticmethod
    def construct_output_files(
            bucket_name: str,
            data_by_sensor_type: dict[SensorType, dict],
            filename_by_sensor_type: dict[SensorType, str]
    ) -> list[S3JsonFile]:
        return [S3JsonFile(
            bucket_name.replace(SUB_COMPONENT_BRONZE, SUB_COMPONENT_SILVER),
            filename_by_sensor_type[sensor_type],
            data_by_sensor_type[sensor_type])
            for sensor_type in data_by_sensor_type]
