import abc
import json

from boto3.dynamodb.conditions import Key, AttributeExists

from conf import settings
from entities.schemas import Node, Story


class DataDriver(abc.ABC):
    @abc.abstractmethod
    def get_story(self, story_id: str):
        pass

    @abc.abstractmethod
    def get_node(self, story_id: str, uri: str):
        pass


class DynamoDBDriver(DataDriver):
    def __init__(self, connection):
        self.connection = connection.Table(settings.STORY_TABLE_NAME)

    def get_story(self, story_id: str):
        response = self.connection.query(KeyConditionExpression=Key("id").eq(story_id),
                                         ProjectionExpression=f"id, root",)
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(json.dumps(response))

        if response["Count"] == 1:
            return Story(**response["Items"][0])

    def get_node(self, story_id: str, uri: str):
        response = self.connection.query(KeyConditionExpression=Key("id").eq(story_id),
                                         FilterExpression=f"attribute_exists(nodes.{uri})",
                                         ProjectionExpression=f"nodes.{uri}",
                                         )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(json.dumps(response))

        if response["Count"] == 1:
            return Node(**response["Items"][0]["nodes"][uri])
