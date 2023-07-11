from dataclasses import dataclass
from datetime import datetime


@dataclass
class BotInfo:
    username: str
    name: str
    description: str
    registered_at: datetime
    registered_by: str
