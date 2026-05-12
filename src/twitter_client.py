import tweepy

from .config import get_twitter_credentials, validate_twitter_credentials


def _make_oauth1_handler(credentials: dict) -> tweepy.OAuthHandler:
    oauth_class = getattr(tweepy, "OAuth1UserHandler", None) or getattr(
        tweepy, "OAuthHandler"
    )
    return oauth_class(
        credentials["api_key"],
        credentials["api_secret"],
        credentials["access_token"],
        credentials["access_token_secret"],
    )


def create_twitter_api() -> tweepy.API:
    credentials = validate_twitter_credentials(get_twitter_credentials())
    auth = _make_oauth1_handler(credentials)
    return tweepy.API(auth, wait_on_rate_limit=True)


def ping_twitter_api() -> dict:
    api = create_twitter_api()
    try:
        user = api.verify_credentials()
    except Exception as exc:
        raise RuntimeError(
            "Twitter API ping failed. Check credentials, network access, and API permissions."
        ) from exc

    if user is None:
        raise RuntimeError("Twitter API returned no authenticated user.")

    return {
        "screen_name": getattr(user, "screen_name", None),
        "user_id": getattr(user, "id_str", None) or getattr(user, "id", None),
        "name": getattr(user, "name", None),
    }
