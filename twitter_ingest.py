import dlt
import requests
from typing import Iterator, Dict, Any

from src.config import get_twitter_credentials, validate_bearer_token

SEARCH_URL = "https://api.x.com/2/tweets/search/recent"
TWEET_FIELDS = ",".join(
    [
        "id",
        "text",
        "author_id",
        "created_at",
        "lang",
        "source",
        "public_metrics",
        "entities",
    ]
)
USER_FIELDS = ",".join(["id", "username", "name", "verified"])


def make_bearer_session() -> requests.Session:
    credentials = get_twitter_credentials()
    bearer_token = validate_bearer_token(credentials)
    session = requests.Session()
    session.headers.update(
        {
            "Authorization": f"Bearer {bearer_token}",
            "User-Agent": "twitter-ingest-pipeline/1.0",
        }
    )
    return session


def fetch_recent_posts(query: str, max_results: int = 100) -> Iterator[Dict[str, Any]]:
    session = make_bearer_session()
    params = {
        "query": query,
        "max_results": min(max_results, 100),
        "tweet.fields": TWEET_FIELDS,
        "expansions": "author_id",
        "user.fields": USER_FIELDS,
    }

    next_token = None
    loaded = 0
    while True:
        if next_token:
            params["next_token"] = next_token
        response = session.get(SEARCH_URL, params=params, timeout=30)
        response.raise_for_status()
        payload = response.json()

        users = {user["id"]: user for user in payload.get("includes", {}).get("users", [])}

        for tweet in payload.get("data", []):
            author_id = tweet.get("author_id")
            author = users.get(author_id, {})
            yield {
                "tweet_id": tweet.get("id"),
                "author_id": author_id,
                "author_username": author.get("username"),
                "author_name": author.get("name"),
                "text": tweet.get("text"),
                "created_at": tweet.get("created_at"),
                "lang": tweet.get("lang"),
                "source": tweet.get("source"),
                "public_metrics": tweet.get("public_metrics"),
                "entities": tweet.get("entities"),
            }
            loaded += 1
            if loaded >= max_results:
                return

        next_token = payload.get("meta", {}).get("next_token")
        if not next_token:
            break


@dlt.source
def twitter_source(query: str = "#BTC", max_results: int = 100):
    """
    dlt source for X recent post search.
    """
    yield from fetch_recent_posts(query, max_results)


if __name__ == "__main__":
    pipeline = dlt.pipeline(
        pipeline_name="twitter_ingest",
        destination="duckdb",
        dataset_name="twitter_data",
    )

    load_info = pipeline.run(twitter_source(query="#BTC", max_results=50))

    print(f"Loaded {load_info.metrics['rows_loaded']} rows into DuckDB.")
    print("DuckDB file: twitter_ingest.duckdb")
