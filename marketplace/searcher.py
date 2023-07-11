import asyncio
from typing import List, Optional
from marketplace.info import get_user_avatar
from models.bot_list_model import BotListResponse
from marketplace.database_manager import manager


async def get_all_bots() -> List[BotListResponse]:
    """
    Get all bots registered in the marketplace.
    """
    bots = manager().get_all_bots()

    tasks = []
    for bot in bots:
        tasks.append(asyncio.ensure_future(get_avatar(bot.username)))
    avatars = await asyncio.gather(*tasks)
    return [
        BotListResponse(
            username=bot[0].username,
            name=bot[0].name,
            description=bot[0].description,
            avatar_url=bot[1]
        ) for bot in zip(bots, avatars)
    ]


async def get_avatar(username: str) -> Optional[str]:
    try:
        return await get_user_avatar(username)
    except Exception:
        return None
