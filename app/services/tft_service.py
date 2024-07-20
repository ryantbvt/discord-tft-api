''' TFT service '''

import requests
import socket
import httpx

from urllib.error import URLError, HTTPError
from python_utils.logging import logging
from app import RIOT_TOKEN, REGIONAL_RIOT_URL

# initial logger
logger = logging.init_logger()

async def get_tft_matches(puuid: str, username: str):
    '''
    Description: gets players matches

    Args:
        puuid: user's player's UUID

    Returns:
        match_list (list[str]): list of matches
    '''
    logger.info(f'Fetching tft matches for: {username}')
    endpoint = f'{REGIONAL_RIOT_URL}/tft/match/v1/matches/by-puuid/{puuid}/ids'

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

    logger.info(f'Successfully fetched {username}\'s tft matches')

    match_list = resp.json()

    return match_list

async def champions_used(match_id: str, puuid: str, username: str):
    '''
    Description: gets top 5 champions in 1 match

    Args:
        match_id: match id

    Returns:
        champ_list (List[str]): List of champions used
    '''
    logger.info(f'Fetching match info for {username} for game {match_id}')
    endpoint = f'{REGIONAL_RIOT_URL}/tft/match/v1/matches/{match_id}'

    try:
        async with httpx.AsyncClient() as client:
            logger.info(f'Calling endpoint: {endpoint}')
            response = await client.get(endpoint, headers={
                'X-Riot-Token': RIOT_TOKEN
            })

        response.raise_for_status()
        match_data = response.json()
        
        logger.info(f'Successfully fetched match info for {match_id}')
        
        participants = match_data['info']['participants']

        for participant in participants:
            if participant['puuid'] == puuid:
                player_data = participant
                logger.info(f'Fetched {username}\'s data from game: {match_id}')

        champ_list = [unit['character_id'] for unit in player_data['units']]
        logger.info(f'Successfully fetched {username}\'s units in game {match_id}')

        return champ_list

    except httpx.HTTPStatusError as e:
        logger.error(f'HTTP error occurred: {e}')
    except httpx.RequestError as e:
        logger.error(f'Error while requesting: {e}')
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')
