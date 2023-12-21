from fastapi import FastAPI
from config_data.config import Config, load_config
from routers import properties

import asyncio

app = FastAPI()

app.include_router(properties.router)
