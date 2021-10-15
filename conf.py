from pydantic import BaseSettings


class Settings(BaseSettings):
    REGION: str = "us-east-1"
    DYNAMODB_HOST: str = "127.0.0.1"
    DYNAMODB_PORT: int = 8000
    STORY_TABLE_NAME: str = "stories"
    DYNAMODB_URL: str = f"http://{DYNAMODB_HOST}:{DYNAMODB_PORT}"
    DATA_SOURCE: str = "dynamodb"


settings = Settings()
