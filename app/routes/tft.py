''' TFT API Integration '''

from fastapi import APIRouter, HTTPException, status
from python_utils.logging import logging
from app.services import riot_accounts

# Initialize logger
logger = logging.init_logger()

# Initialize fastapi router
router = APIRouter()

''' APIs '''

@router.post('/v1/tft/top-champ')
async def top_champ():
    '''
    Description: Gets the top 5 champions that a player used

    Return:
        
    '''