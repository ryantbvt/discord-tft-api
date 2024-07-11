from fastapi import FastAPI
from python_utils.logging import logging

from app.routes import riot_integration

# FastAPI app
app = FastAPI()

# Initialize logger
logger = logging.init_logger()

# Connect routers to main application
app.include_router(riot_integration.router)
logger.info("Application started")