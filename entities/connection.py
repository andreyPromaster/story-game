import abc
import json

from boto3.dynamodb.conditions import Key, AttributeExists


class DataDriver(abc.ABC):
    def __int__(self, data_source):
        self.data_source = data_source

    @abc.abstractmethod
    def get_story(self, story_id: str):
        pass

    @abc.abstractmethod
    def get_node(self, story_id: str, uri: str):
        pass


class DynamoDBDriver(DataDriver):
    def __init__(self, connection):
        self.connection = connection.Table("table_name")

    def get_story(self, story_id: str):
        response = self.connection.query(KeyConditionExpression=Key("id").eq(story_id))
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(json.dumps(response))

        items = response["Items"]
        return items

    def get_node(self, story_id: str, uri: str):
        response = self.connection.query(KeyConditionExpression=Key("id").eq(story_id),
                                         FilterExpression=AttributeExists(f"nodes.{uri}"),
                                         ProjectionExpression=f"nodes.{uri}",
                                         )
        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise Exception(json.dumps(response))

        items = response["Items"]
        return items
