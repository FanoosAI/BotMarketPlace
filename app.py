import logging
from logging.handlers import RotatingFileHandler
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from marketplace import registry
from models import register_model


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
async def public_bots():
    pass


@app.post("/register")
async def register_bot(registry_model: register_model.RegisterBotModel):
    try:
        registry.register_bot(
            registry_model.username,
            registry_model.name,
            registry_model.description,
            registry_model.registered_at,
            registry_model.registered_by
        )
    except ValueError as err:
        return {"error": str(err)}
