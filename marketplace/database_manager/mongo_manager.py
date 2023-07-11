from typing import List, Optional
import datetime
from marketplace.database_manager.bot_info import BotInfo


def get_bot() -> BotInfo:
    pass


def get_all_bots() -> List[BotInfo]:
    raise Exception("mongooooo")


def register_bot(username: str, name: str, description: Optional[str],
                 registered_at: datetime, registered_by: str):
    raise Exception("mongooooo")
