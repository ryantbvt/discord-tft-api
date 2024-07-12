''' Riot Integration API '''

import requests

from fastapi import APIRouter, Depends, HTTPException, status
from python_utils.logging import logging
from app.utils import fetch_secrets

# Initialize logger
logger = logging.init_logger()

# Initialize fastapi router
router = APIRouter()

# load config
secrets = fetch_secrets.fetch_tokens("env")

RIOT_TOKEN = secrets['riot_token']
RIOT_URL = secrets['riot_url']

''' APIs '''

@router.get("/v1/champ-rotation")
async def get_champ_rotation():
    '''
    Description: Gets current list of champions from free rotation

    Return:
        champion_list: List[str] of champions
    '''
    logger.info("Received Request: /v1/champion-rotation")

    endpoint = RIOT_URL + '/lol/platform/v3/champion-rotations'

    try:
        logger.info(f'Calling endpoint: {endpoint}')

        resp = requests.get(endpoint, headers={
            'X-Riot-Token': RIOT_TOKEN
        })

    except requests.exceptions.HTTPError as http_err:
        logger.error(f'HTTP error occurred: {http_err}')  # Log HTTP errors (e.g., 404, 500)
        raise HTTPException(
            status_code=resp.status_code,
            detail=f'HTTP error occurred: {http_err}'
        )
    except requests.exceptions.RequestException as req_err:
        logger.error(f'Request exception occurred: {req_err}')  # Log other request-related errors (e.g., connection issues)
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
            detail=f'Request exception occurred: {req_err}'
        )
    except Exception as e:
        logger.error(f'An unexpected error occurred: {e}')  # Log any other exceptions
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f'An unexpected error occurred: {e}'
        )
    
    # Store JSON of all free champs, new players + normal rotation
    logger.info('Successfully fetched free champion rotation')
    all_champ_ids = resp.json()

    new_champ_rotation = all_champ_ids['freeChampionIdsForNewPlayers']
    champ_rotation = all_champ_ids['freeChampionIds']

    print(champ_rotation)

    logger.info("Completed Request: /v1/champion-rotation")
