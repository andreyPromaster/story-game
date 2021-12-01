from conf import settings

from .data_source import DataDriver
from .dynamo_db.data_source import DynamoDBDriver
from .sqlalchemy.data_source import RDSDriver

DATA_SOURCES = {
    "dynamodb": DynamoDBDriver,
    "rds": RDSDriver,
}


def get_data_source() -> DataDriver:
    driver_cls = DATA_SOURCES.get(settings.DATA_SOURCE)
    if driver_cls is None:
        raise ValueError("Unknown driver name")
    driver = driver_cls()
    return driver
