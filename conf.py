from pydantic import BaseSettings


class Settings(BaseSettings):
    REGION: str = "us-east-1"
    STORY_TABLE_NAME: str = "stories"
    DYNAMODB_URL: str = "http://127.0.0.1:8000"
    DATA_SOURCE: str = "dynamodb"
    LOCAL: int = 1


settings = Settings()
