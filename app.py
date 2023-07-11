import logging
from logging.handlers import RotatingFileHandler
from typing import List

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from marketplace import registry, searcher
from models import register_model, bot_list_model

app = FastAPI()
# handle corse
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# configure logging

logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)s %(levelname)s %(message)s",
)
file_handler = RotatingFileHandler(
    "logs/marketplace.log",
    maxBytes=1048576,  # 1 MB
    backupCount=3
)
file_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(file_handler)

stream_handler = logging.StreamHandler()
stream_handler.setLevel(logging.DEBUG)
logging.getLogger().addHandler(stream_handler)


@app.get("/")
async def root():
    return {"message": "Welcome to the BOT Marketplace backend server."
                       " See /docs for api documentations."}


@app.get("/public-bots")
async def public_bots() -> List[bot_list_model.BotListResponse]:
    return await searcher.get_all_bots()


@app.post("/register")
async def register_bot(request: Request, registry_model: register_model.RegisterBotModel) -> \
        register_model.RegisterBotResponse:
    registry.register_bot(
        request,
        registry_model.username,
        registry_model.name,
        registry_model.description,
        registry_model.registered_at,
        registry_model.registered_by
    )
    return register_model.RegisterBotResponse(
        message=f"Bot {registry_model.username} registered successfully.")
