import asyncio
import discord
import dotenv
import os
import re
import time
from web3 import Web3
from discord.ext import commands
from utils.logger import logger
from typing import List, Optional
from client import client as bot
from env import get_env_file


startup_time: float = 0.0


def set_start_time(time: float):
    """
    Sets global startup_time to the inputted time.
    """
    global startup_time
    startup_time = time


def get_uptime() -> float:
    """
    Returns uptime in seconds.
    """
    return time.perf_counter() - startup_time


async def shutdown(signal, loop):
    """Cleanup tasks tied to the service's shutdown."""
    logger.info(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logger.info(f"Cancelling {len(tasks)} outstanding tasks")
    await asyncio.gather(*tasks)
    logger.info("Stopping loop")
    loop.stop()
    logger.info("Loop stopped")


async def send_embed_dm(
    member: discord.Member, embed: discord.Embed, ctx: Optional[commands.Context] = None
):
    try:
        await member.send(embed=embed)
    except Exception as e:
        logger.error(e)
        path = (
            "'Privacy Settings'" " -> " "'Allow direct messages from server members.'"
        )
        if ctx is not None:
            await ctx.send(
                (
                    "{} Please enable {} for this server " "to verify your account."
                ).format(member.mention, path)
            )


def get_guild(guild_id: str) -> Optional[discord.Guild]:
    return bot.get_guild(int(guild_id))


def get_member(user_id: str, guild: discord.Guild) -> Optional[discord.Member]:
    return guild.get_member(int(user_id))


def get_all_nft_addresses() -> List[str]:
    dotenv.load_dotenv(get_env_file())
    prefix = "NFT_"
    pattern = re.compile(r'{prefix}\w+'.format(prefix=prefix))
    addresses = [val for key, val in os.environ.items() if pattern.match(key)
                 and Web3.isAddress(val)]
    return addresses
