from app.utils import fetch_secrets

# load config
secrets = fetch_secrets.fetch_tokens("env")

RIOT_TOKEN = secrets['riot_token']
RIOT_URL = secrets['riot_url']
REGIONAL_RIOT_URL = secrets['regional_riot_url']
