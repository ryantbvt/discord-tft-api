''' Riot Integration API '''

from fastapi import APIRouter, Depends, HTTPException, status
from python_utils.logging import logging

# Initialize logger
logger = logging.init_logger()

# Initialize fastapi router
router = APIRouter()

@router.get("/champ-rotation")
async def get_champ_rotation():
    '''
    Description: Gets current list of champions from free rotation

    Return:
        champion_list: List[str] of champions
    '''
    pass