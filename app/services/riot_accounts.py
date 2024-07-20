''' Access Riot Account Information '''

import requests
import socket

from urllib.error import URLError, HTTPError
from python_utils.logging import logging
from app import RIOT_TOKEN, REGIONAL_RIOT_URL

# Initialize logger
logger = logging.init_logger()

async def get_account_info(account_name: str, tag_line: str) -> dict:
    '''
    Description: get riot account information

    Args:
        account_name: in-game username
        tag_line: tag line for player. (Example: NA1)

    Returns:
        account_info (dict): account information of player
    '''
    logger.info(f'Fetching account info for: {account_name}#{tag_line}')
    endpoint = f'{REGIONAL_RIOT_URL}/riot/account/v1/accounts/by-riot-id/{account_name}/{tag_line}'

    try:
        logger.info(f'Calling endpoint: {endpoint}')
        resp = requests.get(endpoint, headers={
            'X-Riot-Token': RIOT_TOKEN
        })

    except HTTPError as e:
        logger.error(f'HTTP error occurred: {e.code} {e.reason}')
    except URLError as e:
        logger.error(f"Failed to reach the server: {e.reason}")
    except socket.timeout:
        logger.error("The request timed out")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    logger.info(f'Successfully fetch account info for: {account_name}#{tag_line}')

    # Convert data to a form we want
    account_info_data = resp.json()
    account_info = {
        'puuid': account_info_data['puuid'],
        'game_name':account_info_data['gameName'],
        'tag_line': account_info_data['tagLine']
    }

    # Return account information
    logger.info(f'Return account information for: {account_name}#{tag_line}')
    return account_info
