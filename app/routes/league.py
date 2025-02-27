''' League of Legends Integration API '''

import requests

from fastapi import APIRouter, HTTPException, status
from python_utils.logging import logging
from app.services import ddragon_league
from app import RIOT_URL, RIOT_TOKEN

# Initialize logger
logger = logging.init_logger()

# Initialize fastapi router
router = APIRouter()

''' APIs '''

@router.get("/v1/lol/champ-rotation")
async def get_champ_rotation(new_players=False):
    '''
    Description: Gets current list of champions from free rotation

    Return:
        champion_list: List[str] of champions
    '''
    logger.info("Received Request: /v1/lol/champ-rotation")

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
    logger.info('Successfully fetched free champion rotation as key')
    all_champ_ids = resp.json()

    new_champ_rotation = all_champ_ids['freeChampionIdsForNewPlayers']
    champ_rotation = all_champ_ids['freeChampionIds']

    champ_rotation_name = []

    # convert champion key to champion names
    if new_players:
        for champ_key in new_champ_rotation:
            champ_info = await ddragon_league.get_champion_by_key(champ_key)
            champ_name = champ_info['name']

            champ_rotation_name.append(champ_name)

    else:
        for champ_key in champ_rotation:
            champ_info = await ddragon_league.get_champion_by_key(champ_key)
            champ_name = champ_info['name']

            champ_rotation_name.append(champ_name)

    logger.info("Completed Request: /v1/lol/champ-rotation")
    return champ_rotation_name
