''' Fetch configs '''

import os

from python_utils.logging import logging
from dotenv import load_dotenv

logger = logging.init_logger()

def fetch_tokens(run_type: str):
    '''
    Description: Fetches secret tokens

    Args:
        run_type: defines method of fetching configs

    Returns:
        secrets: list of secrets needed to run the bot
    '''
    logger.info("Running fetch_tokens")

    secrets = {
        "riot_url": None,
        "riot_token": None,
        "accounts_riot_url": None
    }

    if run_type == "container":
        logger.info("Fetching tokens from config.yaml")
        pass

    else:
        logger.info("Fetching tokens from .env")

        load_dotenv()
        RIOT_URL = os.getenv('RIOT_URL')
        RIOT_TOKEN = os.getenv('RIOT_TOKEN')
        ACCOUNTS_RIOT_URL = os.getenv('ACCOUNTS_RIOT_URL')

    logger.info("Successfully obtained token")

    secrets['riot_url'] = RIOT_URL
    secrets['riot_token'] = RIOT_TOKEN
    secrets['accounts_riot_url'] = ACCOUNTS_RIOT_URL

    logger.info("Returning secrets")
    return secrets