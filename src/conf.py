from pydantic import BaseSettings


class Settings(BaseSettings):
    REGION: str = "us-east-1"
    STORY_TABLE_NAME_DYNAMODB: str = "stories"
    DYNAMODB_URL: str = "http://127.0.0.1:8000"
    DATA_SOURCE: str = "dynamodb"
    LOCAL: bool = True

    # RDS setting
    DB_USER: str = "postgres"
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_NAME: str = "game_story"
    DB_PASS: str = ""


settings = Settings()
