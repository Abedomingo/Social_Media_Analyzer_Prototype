import os
from pathlib import Path

from dotenv import load_dotenv


dotenv_path = Path(".env")
if dotenv_path.exists():
    load_dotenv(dotenv_path)


def get_twitter_credentials() -> dict:
    return {
        "api_key": os.getenv("TWITTER_API_KEY"),
        "api_secret": os.getenv("TWITTER_API_SECRET_KEY"),
        "access_token": os.getenv("TWITTER_ACCESS_TOKEN"),
        "access_token_secret": os.getenv("TWITTER_ACCESS_TOKEN_SECRET"),
        "bearer_token": os.getenv("TWITTER_BEARER_TOKEN"),
    }


def validate_twitter_credentials(credentials: dict) -> dict:
    required = [
        "api_key",
        "api_secret",
        "access_token",
        "access_token_secret",
    ]
    missing = [name for name in required if not credentials.get(name)]
    if missing:
        raise ValueError(
            "Missing Twitter credentials in environment variables: "
            + ", ".join(missing)
        )
    return credentials


def validate_bearer_token(credentials: dict) -> str:
    bearer_token = credentials.get("bearer_token")
    if not bearer_token:
        raise ValueError(
            "Missing Twitter bearer token in environment variables: TWITTER_BEARER_TOKEN"
        )
    return bearer_token
