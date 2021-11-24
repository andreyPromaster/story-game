from conf import settings

from .data_source import DataDriver
from .dynamo_db.data_source import DynamoDBDriver


def get_data_source() -> DataDriver:
    if settings.DATA_SOURCE == "dynamodb":
        return DynamoDBDriver()
