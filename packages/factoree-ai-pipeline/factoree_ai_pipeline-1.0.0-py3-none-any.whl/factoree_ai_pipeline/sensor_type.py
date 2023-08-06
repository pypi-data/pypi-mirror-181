from enum import Enum

FLOAT = 'float'
INT = 'int'
BOOLEAN = 'boolean'
DATA_TYPE = 'data_type'
NAME_KEY = 'name'


class SensorType(Enum):
    II = {DATA_TYPE: FLOAT, NAME_KEY: 'ii'}
    FI = {DATA_TYPE: FLOAT, NAME_KEY: 'fi'}
    FIC = {DATA_TYPE: FLOAT, NAME_KEY: 'fic'}
    LI = {DATA_TYPE: FLOAT, NAME_KEY: 'li'}
    LIC = {DATA_TYPE: FLOAT, NAME_KEY: 'lic'}
    TI = {DATA_TYPE: FLOAT, NAME_KEY: 'ti'}
    TIC = {DATA_TYPE: FLOAT, NAME_KEY: 'tic'}
    WI = {DATA_TYPE: FLOAT, NAME_KEY: 'wi'}
    WIC = {DATA_TYPE: FLOAT, NAME_KEY: 'wic'}
    STEP = {DATA_TYPE: INT, NAME_KEY: 'step'}
    A = {DATA_TYPE: BOOLEAN, NAME_KEY: 'a'}
    CV = {DATA_TYPE: BOOLEAN, NAME_KEY: 'cv'}
    P = {DATA_TYPE: BOOLEAN, NAME_KEY: 'p'}
    AI = {DATA_TYPE: FLOAT, NAME_KEY: 'ai'}
    AS = {DATA_TYPE: FLOAT, NAME_KEY: 'as'}
    DI = {DATA_TYPE: FLOAT, NAME_KEY: 'di'}
    FQ = {DATA_TYPE: FLOAT, NAME_KEY: 'fq'}
    HIC = {DATA_TYPE: FLOAT, NAME_KEY: 'hic'}
    LSH = {DATA_TYPE: FLOAT, NAME_KEY: 'lsh'}
    PHI = {DATA_TYPE: FLOAT, NAME_KEY: 'phi'}
    PI = {DATA_TYPE: FLOAT, NAME_KEY: 'pi'}
    PIC = {DATA_TYPE: FLOAT, NAME_KEY: 'pic'}
    VI = {DATA_TYPE: FLOAT, NAME_KEY: 'vi'}
    WQ = {DATA_TYPE: FLOAT, NAME_KEY: 'wq'}
    ZI = {DATA_TYPE: FLOAT, NAME_KEY: 'zi'}


def parse_sensor_type(token: str) -> SensorType | None:
    parsed_sensor_type = None
    for value in SensorType:
        if value.value[NAME_KEY] == token.lower():
            parsed_sensor_type = value
    return parsed_sensor_type
