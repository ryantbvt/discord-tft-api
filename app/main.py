from fastapi import FastAPI
from python_utils.logging import logging

from app.routes import league, tft

# FastAPI app
app = FastAPI()

# Initialize logger
logger = logging.init_logger()

# Connect routers to main application
app.include_router(league.router)
app.include_router(tft.router)
logger.info("Application started")