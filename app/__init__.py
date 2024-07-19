from app.utils import fetch_secrets

# load config
secrets = fetch_secrets.fetch_tokens("env")

RIOT_TOKEN = secrets['riot_token']
RIOT_URL = secrets['riot_url']
ACCOUNTS_RIOT_URL = secrets['accounts_riot_url']
