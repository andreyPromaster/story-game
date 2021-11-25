from conf import settings

from .data_source import DataDriver
from .dynamo_db.data_source import DynamoDBDriver
from .sqlalchemy.data_source import RDSDriver


def get_data_source() -> DataDriver:
    if settings.DATA_SOURCE == "dynamodb":
        return DynamoDBDriver()
    elif settings.DATA_SOURCE == "rds":
        return RDSDriver()
