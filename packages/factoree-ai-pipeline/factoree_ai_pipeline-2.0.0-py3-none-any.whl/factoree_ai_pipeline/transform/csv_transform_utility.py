from datetime import datetime
from logging import Logger
from factoree_ai_pipeline.file.file_utils import get_silver_file_name
from factoree_ai_pipeline.sensor_type import SensorType, parse_sensor_type
from factoree_ai_pipeline.transform.transform_utility import TransformUtility, TransformationInnerOutput, DATA_KEY, \
    TIME_KEY, PHASE_ID_KEY, VALUES_KEY, ERRORS_KEY, DATA_TYPE_KEY

Csv = list[list[int | float | str | datetime]]


class CsvTransformUtility(TransformUtility[Csv]):
    def __init__(
            self,
            time_zone: str,
            timestamp_column: int,
            logger: Logger,
            is_test: bool = False
    ):
        super(CsvTransformUtility, self).__init__(time_zone, logger, is_test)
        self.timestamp_column = timestamp_column

    def standardize_file_data(self, file_data: Csv) -> (Csv, Csv):
        standardized_data: Csv = []
        unrecognized_sensor_type_tags: Csv = []
        for i in range(self.timestamp_column + 1, len(file_data[0])):
            sensor_type = self.extract_sensor_type(file_data[0][i])
            if sensor_type is None:
                for row in range(len(file_data)):
                    if len(unrecognized_sensor_type_tags) <= row:
                        unrecognized_sensor_type_tags.append([file_data[row][self.timestamp_column]])

                    unrecognized_sensor_type_tags[row].append(file_data[row][i])
            else:
                for row in range(len(file_data)):
                    if len(standardized_data) <= row:
                        standardized_data.append(
                            [self.standardize_value(sensor_type, file_data[row][self.timestamp_column])]
                        )

                    standardized_data[row].append(self.standardize_value(sensor_type, file_data[row][i]))

        return standardized_data, unrecognized_sensor_type_tags

    def transform_data_to_silver_format(
            self, standardized_data: Csv
    ) -> (dict[SensorType, dict], dict[SensorType, str], Csv):
        columns_by_sensor_type = self.group_columns_by_sensor_type(standardized_data)
        transformed_data_by_sensor_type, filenames = self.transform_grouped_data_to_silver_format(
            columns_by_sensor_type,
            standardized_data
        )
        return TransformationInnerOutput(
            transformed_data_by_sensor_type,
            filenames
        )

    def transform_grouped_data_to_silver_format(
            self, columns_by_sensor_type: dict[SensorType, list[int]], standardized_data: Csv
    ) -> (dict[SensorType, dict], dict[SensorType, str]):
        transformed_data_by_sensor_type: dict[SensorType, dict] = {}
        filenames: dict[SensorType, str] = self.get_silver_filenames(columns_by_sensor_type, standardized_data)

        for sensor_type in columns_by_sensor_type.keys():
            data_of_sensor_type = transformed_data_by_sensor_type.get(sensor_type, {DATA_KEY: []})
            for row in range(1, len(standardized_data)):
                if sensor_type == SensorType.STEP:
                    data_of_sensor_type.get(DATA_KEY).append({
                        TIME_KEY: standardized_data[row][self.timestamp_column],
                        PHASE_ID_KEY: standardized_data[row][columns_by_sensor_type.get(sensor_type)[0]]
                    })
                else:
                    values = {}
                    errors = {}
                    for column in columns_by_sensor_type.get(sensor_type):
                        if self.is_data_type_mismatch(standardized_data[row][column], sensor_type):
                            errors[standardized_data[0][column]] = standardized_data[row][column]
                        else:
                            values[standardized_data[0][column]] = standardized_data[row][column]

                    data_of_sensor_type.get(DATA_KEY).append({
                        TIME_KEY: standardized_data[row][self.timestamp_column],
                        VALUES_KEY: values,
                        ERRORS_KEY: errors
                    })

            transformed_data_by_sensor_type[sensor_type] = data_of_sensor_type

        return transformed_data_by_sensor_type, filenames

    def group_columns_by_sensor_type(self, file_data: Csv) -> dict[SensorType, list[int]]:
        result: dict[SensorType, list[int]] = {}

        for i in range(1, len(file_data[0])):
            parsed_type: SensorType = self.extract_sensor_type(file_data[0][i])
            columns_of_type = result.get(parsed_type, [])
            columns_of_type.append(i)
            result[parsed_type] = columns_of_type

        return result

    # noinspection PyMethodMayBeStatic
    def extract_sensor_type(self, tag: str) -> SensorType:
        tag_parts = tag.split('-')
        return parse_sensor_type(tag_parts[1]) or parse_sensor_type(tag_parts[2])

    def get_silver_filenames(
            self, columns_by_sensor_type: dict[SensorType, list[int]], standardized_data: Csv
    ) -> dict[SensorType, str]:
        filenames: dict[SensorType, str] = {}
        for sensor_type in columns_by_sensor_type.keys():
            if sensor_type not in filenames.keys():
                filenames[sensor_type] = self.get_silver_filename_for_sensor_type_samples(
                    sensor_type,
                    standardized_data,
                    columns_by_sensor_type.get(sensor_type)[0]
                )
        return filenames

    def get_silver_filename_for_sensor_type_samples(
            self,
            sensor_type: SensorType,
            standardized_data: Csv,
            column: int
    ) -> str:
        tag = standardized_data[0][column]
        first_sample = self.localize_datetime(standardized_data[1][self.timestamp_column])
        last_sample = self.localize_datetime(standardized_data[-1][self.timestamp_column])
        facility = tag.split('-')[0]

        if sensor_type == SensorType.STEP:
            result = get_silver_file_name(
                sensor_type.value.get(DATA_TYPE_KEY),
                facility,
                sensor_type.name,
                first_sample,
                last_sample,
                self.is_test,
                tag.split('-')[1]
            )
        else:
            result = get_silver_file_name(
                sensor_type.value.get(DATA_TYPE_KEY),
                facility,
                sensor_type.name,
                first_sample,
                last_sample,
                self.is_test
            )
        return result

    def localize_datetime(self, utc_time: datetime):
        return datetime(
            utc_time.year, utc_time.month, utc_time.day, utc_time.hour, utc_time.minute, utc_time.second,
            tzinfo=self.zone_info
        ) + self.zone_info.utcoffset(utc_time)
