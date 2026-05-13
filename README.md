# Social Media Analyzer
This project is back in prototype stage. Right now, overgoing a total refactoring in order to support ETL pipelines that store, normalize and clean PII from records obtained via the X/Twitter API.

# Notes for Abraham
* Data has been normalized
* Managed to collect the 100 bots from #Covid. The first couple groups were just sparse by chance
* We should look at the average bot score of all users sampled. Some hashtags had many people with scores higher than 3 but less than our threshhold

## Credential storage update

This project now uses a local `.env` file for Twitter API credentials instead of the legacy `twitter_api_key_config.yaml`.

- `twitter_api_key_config.yaml` has been removed from the repository and is no longer used.
- Use `.env.example` as a starting point.

## Getting started

1. Create a virtual environment and install dependencies:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   python -m pip install -r requirements.txt
   ```

2. Store Twitter credentials securely.
   - Option A: create a local `.env` file from `.env.example`
   - Option B: export shell environment variables in your terminal or shell profile

   Required variables:
   ```bash
   export TWITTER_API_KEY=your_api_key
   export TWITTER_API_SECRET_KEY=your_api_secret_key
   export TWITTER_ACCESS_TOKEN=your_access_token
   export TWITTER_ACCESS_TOKEN_SECRET=your_access_token_secret
   ```

3. Run the Twitter ping script:

   ```bash
   python ping_twitter.py
   ```

> Important: Do not commit `.env` or any file containing your Twitter credentials.
