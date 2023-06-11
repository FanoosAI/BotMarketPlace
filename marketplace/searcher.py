import asyncio
from typing import List, Optional

from marketplace import get_db_cursor
from marketplace.info import get_user_avatar
from models.bot_list_model import BotListResponse


async def get_all_bots() -> List[BotListResponse]:
    """
    Get all bots registered in the marketplace.
    """
    with get_db_cursor() as cursor:
        cursor.execute("SELECT * FROM bots")
        bots = cursor.fetchall()

    tasks = []
    for bot in bots:
        tasks.append(asyncio.ensure_future(get_avatar(bot[0])))
    avatars = await asyncio.gather(*tasks)
    return [
        BotListResponse(
            username=bot[0][0],
            name=bot[0][1],
            description=bot[0][2],
            avatar_url=bot[1]
        ) for bot in zip(bots, avatars)
    ]


async def get_avatar(username: str) -> Optional[str]:
    try:
        return await get_user_avatar(username)
    except Exception:
        return None
