import json

import boto3
from boto3.dynamodb.conditions import Key
from botocore.config import Config

from common.entities.schemas import Node, Story, StoryList
from conf import DynamoDBSettings, settings
from data_storage.data_source import DataDriver
from utilities.exceptions import DynamoDBError


def get_connection():
    dynamo_settings = DynamoDBSettings()
    config = Config(retries={"max_attempts": 1, "mode": "standard"})
    if settings.LOCAL:
        conn = boto3.resource(
            "dynamodb",
            endpoint_url=dynamo_settings.DYNAMODB_URL,
            config=config,
            region_name=dynamo_settings.REGION,
        )
    else:
        conn = boto3.resource(
            "dynamodb",
            config=config,
        )
    return conn.Table(dynamo_settings.STORY_TABLE_NAME_DYNAMODB)


class DynamoDBDriver(DataDriver):
    def __init__(self, connection=None):
        self.connection = connection or get_connection()

    def get_story(self, story_id: str):
        response = self.connection.query(
            KeyConditionExpression=Key("id").eq(story_id),
            ProjectionExpression="id, root, #name",
            ExpressionAttributeNames={
                "#name": "name"
            },  # We should use an alias for any reserved word
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DynamoDBError(json.dumps(response))

        if response["Count"] == 1:
            return Story(**response["Items"][0])
        return None

    def get_node(self, story_id: str, uri: str):
        response = self.connection.query(
            KeyConditionExpression=Key("id").eq(story_id),
            FilterExpression=f"attribute_exists(nodes.{uri})",
            ProjectionExpression=f"nodes.{uri}",
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DynamoDBError(json.dumps(response))

        if response["Count"] == 1:
            return Node(**response["Items"][0]["nodes"][uri])
        return None

    def get_story_list(self):
        response = self.connection.scan(
            ProjectionExpression="id, root, #name",
            ExpressionAttributeNames={"#name": "name"},
        )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DynamoDBError(json.dumps(response))
        return StoryList(stories=response["Items"])
