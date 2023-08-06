import json
import re
from abc import ABC, abstractmethod
from typing import TypeVar, Generic
from datetime import datetime
from logging import Logger
from factoree_ai_pipeline.transform.csv_transform_utility import Csv

T = TypeVar('T')


class TextParser(ABC, Generic[T]):
    def __init__(self, logger: Logger):
        self.logger = logger

    @abstractmethod
    def parse(self, text: str) -> T:
        pass


class CsvParser(TextParser[Csv]):
    def __init__(
            self,
            logger: Logger,
            datetime_format: str | None = None,
            timestamp_column: int | None = None
    ):
        super().__init__(logger)
        if datetime_format is None or timestamp_column is None:
            self.timestamp_column = None
        else:
            self.timestamp_column = timestamp_column
            self.datetime_format = datetime_format

    def parse(self, text: str) -> Csv:
        grid = []
        for line in text.split("\n"):
            if line.strip():
                line_main_body = re.findall(r'(.*[^,]),*$', line.strip())[0]
                grid.append(line_main_body.split(","))

        for i in range(len(grid)):
            for j in range(len(grid[i])):
                grid[i][j] = self.__convert(grid[i][j], j)

        return grid

    def __convert(self, value: str, column: int) -> any:
        if value.isnumeric():
            return int(value)

        if re.match(r'^-\d+$', value) is not None:
            return int(value)

        if re.search(r'^-?\d+\.\d+$', value) is not None:
            return float(value)

        if re.search(r'^-?\d+[Ee][-+]?\d+$', value) is not None:
            return float(value)

        if re.search(r'^-?\d+\.\d+[Ee][-+]?\d+$', value) is not None:
            return float(value)

        if column == self.timestamp_column and value:
            try:
                return datetime.strptime(value, self.datetime_format)
            except ValueError as e:
                self.logger.error(f'Failed to parsing date and time: [{value}]')
                raise e

        return value


class JsonParser(TextParser[dict]):
    def parse(self, text: str) -> dict:
        return json.loads(text)
