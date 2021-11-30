from pydantic import BaseSettings


class Settings(BaseSettings):
    DATA_SOURCE: str = "dynamodb"
    LOCAL: bool = True


class DynamoDBSettings(BaseSettings):
    REGION: str = "us-east-1"
    STORY_TABLE_NAME_DYNAMODB: str = "stories"
    DYNAMODB_URL: str = "http://127.0.0.1:8000"


class RDSSettings(BaseSettings):
    DB_USER: str = "postgres"
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_NAME: str = "game_story"
    DB_PASS: str = ""


settings = Settings()
