''' DataDragon functions '''

import json
import socket

from urllib.request import urlopen
from urllib.error import URLError, HTTPError
from python_utils.logging import logging

# Initialize logger
logger = logging.init_logger()

# Cache for champion data
champion_by_id_cache = {}
champion_json = {}

# Data Dragon Version URL
ddragon_base_url = 'http://ddragon.leagueoflegends.com'

# This is an example of champion data: https://ddragon.leagueoflegends.com/cdn/14.13.1/data/en_US/champion.json

async def get_latest_ddragon_version():
    '''
    Description: Get data from data dragon

    Returns:
        data_json: JSON from ddragon or None if error
    '''
    endpoint = '/api/versions.json'
    versions_url = ddragon_base_url + endpoint
    
    try:
        logger.info(f'Getting latest ddragon champion version: {versions_url}')
        
        with urlopen(versions_url) as resp:
            versions = json.loads(resp.read())

            logger.info(f'Return latest league patch: {versions[0]}')
            return versions[0]
    
    except Exception as e:
        logger.error(f"Error fetching versions: {e}")
        return None    


async def get_latest_champion_ddragon(lang='en_US'):
    '''
    Description: Get latest champion data from Data Dragon

    Args:
        lang: language to get data

    Returns:
        data_json (dict): Parsed JSON data from response or None if errors
    '''
    # Check if we already have data cached
    if lang in champion_json:
        return champion_json[lang]

    # Get latest patch
    version = await get_latest_ddragon_version()
    if not version:
        return None
    
    # Construct latest champ data dragon url
    ddragon_url = f'{ddragon_base_url}/cdn/{version}/data/{lang}/champion.json'

    try:
        logger.info(f'Getting latest ddragon champion data: {ddragon_url}')

        with urlopen(ddragon_url) as resp:
            data_json = json.loads(resp.read())
            champion_json[lang] = data_json

            logger.info('Cached and return champion json')
            return data_json
    
    except HTTPError as e:
        logger.error(f'HTTP error occurred: {e.code} {e.reason}')
    except URLError as e:
        logger.error(f"Failed to reach the server: {e.reason}")
    except socket.timeout:
        logger.error("The request timed out")
    except Exception as e:
        logger.error(f"An unexpected error occurred: {e}")

    return None

async def get_champion_by_key(key, lang='en_US'):
    '''
    Description: Get champion name by champion key

    Args:
        key: Champion key
        lang: Language of data

    Returns:
        champ_info (dict): Champion data or None if not found. To access name, simply use ['name']
    '''
    # Checks if data is cached
    if lang not in champion_by_id_cache:
        logger.info('Grabbing champion data')
        json_data = await get_latest_champion_ddragon(lang)
        if not json_data:
            return None
        
        champion_by_id_cache[lang] = {}
        for _, champ_info in json_data['data'].items():
            champion_by_id_cache[lang][champ_info['key']] = champ_info
        
        logger.info('Champion data cached')

    champ_info = champion_by_id_cache[lang].get(str(key))
    if champ_info is None:
        logger.warning(f'Champion key, {key}, not found')
        return None

    # logger.info(f'Returning champion info for: {champ_info["name"]}')
    return champ_info

async def get_champion_by_id(name, lang='en_US'):
    '''
    Get champion data by name

    Args:
        name: Champion name
        language: Language to get data

    Returns:
        champ_info (dict): Champion data or None if not found
    '''
    # Checks if data is cached
    json_data = await get_latest_champion_ddragon(lang)
    if not json_data:
        return None
    
    logger.info(f'Getting champ info by champion name: {name}')
    champ_info = json_data['data'].get(name)

    logger.info(f'Returning champion info for: {name}')
    return champ_info
