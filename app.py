import boto3
from botocore.config import Config

from conf import settings
from entities.connection import DynamoDBDriver


def test():
    conf = Config(retries={"max_attempts": 1, "mode": "standard"})

    conn = boto3.resource(
        "dynamodb", endpoint_url=f"http://{settings.DYNAMODB_HOST}:{settings.DYNAMODB_PORT}", config=conf,
        region_name=settings.REGION)

    source = DynamoDBDriver(conn)
    node = source.get_node("test", "Root")
    print(node)
    story = source.get_story("test")
    print(story)

if __name__ == "__main__":
    test()
