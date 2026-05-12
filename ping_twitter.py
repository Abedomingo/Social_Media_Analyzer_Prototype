from src.twitter_client import ping_twitter_api


def main() -> None:
    result = ping_twitter_api()
    print("Twitter API authenticated successfully:")
    print(f"  screen_name: {result['screen_name']}")
    print(f"  user_id: {result['user_id']}")
    print(f"  name: {result['name']}")


if __name__ == "__main__":
    main()
