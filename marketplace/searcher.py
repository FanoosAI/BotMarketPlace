from typing import List, Optional

from marketplace import get_db_cursor
from marketplace.info import get_user_avatar
from models.bot_list_model import BotListResponse


def get_all_bots() -> List[BotListResponse]:
    """
    Get all bots registered in the marketplace.
    """
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM bots")
        bots = cursor.fetchall()
    return [
        BotListResponse(
            username=bot[0],
            name=bot[1],
            description=bot[2],
            avatar_url=get_avatar(bot[0])
        ) for bot in bots
    ]


def get_avatar(username: str) -> Optional[str]:
    try:
        return get_user_avatar(username)
    except Exception:
        return None
