from typing import Optional
from pydantic import BaseModel


class BotListResponse(BaseModel):
    username: str
    name: str
    description: Optional[str]
    avatar_url: Optional[str]
