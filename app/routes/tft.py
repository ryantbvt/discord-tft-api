''' TFT API Integration '''

import asyncio

from fastapi import APIRouter, HTTPException, status
from python_utils.logging import logging
from app.services import riot_accounts, tft_service
from app.models import riot_user

# Initialize logger
logger = logging.init_logger()

# Initialize fastapi router
router = APIRouter()

''' APIs '''

@router.post('/v1/tft/top-champ')
async def top_champ(riot_user: riot_user.RiotUser):
    '''
    Description: Gets the top 5 champions that a player used

    Args:
        RiotUser:
            username: in-game username of player
            tag_line: player's tag line

    Return:
        top_5_champs_names (List[str]): List of the top 5 champs used from player
    '''
    logger.info("Received Request: /v1/tft/top-champ")
    account_info = await riot_accounts.get_account_info(riot_user.username, riot_user.tag_line)
    match_list = await tft_service.get_tft_matches(account_info['puuid'], account_info['game_name'])
    
    unit_dict = {}

    logger.info(f"Fetching top champions used for {account_info['game_name']} in past {len(match_list)} games")

    tasks = [] # list of commands to run

    for match in match_list:
        tasks.append(tft_service.champions_used(match, account_info['puuid'], account_info['game_name']))

    results = await asyncio.gather(*tasks) # asyncio.gather will run all of the tasks in the list concurrently

    for champ_list in results:
        for unit in champ_list:
            if unit in unit_dict:
                unit_dict[unit] += 1
            else:
                unit_dict[unit] = 1
    
    top_5_champs = sorted(unit_dict.items(), key=lambda item: item[1], reverse=True)[:5]
    top_5_champs_names = [unit for unit, _ in top_5_champs]

    logger.info("Completed Request: /v1/tft/top-champ")
    return top_5_champs_names
