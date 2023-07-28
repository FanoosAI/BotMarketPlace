from datetime import datetime

from pydantic import BaseModel


class RegisterBotModel(BaseModel):
    username: str
    name: str
    description: str
    registered_at: datetime
    registered_by: str


class RegisterBotResponse(BaseModel):
    message: str


class RemoveBotModel(BaseModel):
    username: str
    bot_username: str
