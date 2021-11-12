import asyncio
import discord
import json
import time
from discord.ext import commands
from utils.logger import logger
from typing import List, Optional, TypedDict
from client import client as bot


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


class GuildConfig(TypedDict):
    name: str
    guild_id: str
    addresses: List[str]
    token_holder_role: str
    renting_role: str


def get_config_for_guild(guild_id: str) -> Optional[GuildConfig]:
    """
    Assumes guild_nfts_config.json is valid

    Example:

    [
      {
        "name": "<name>",
        "guild_id": "<guild_id>",
        "addresses": ["<address0>", "<address1>"],
        "token_holder_role": "<token_holder_role>",
        "renting_role": "<renting_role>"
      }
    ]

    """
    try:
        with open("guild_nfts_config.json", "r") as f:
            data = json.load(f)
            for guild_config in data:
                if guild_config["guild_id"] == guild_id:
                    return guild_config
            return None
    except FileNotFoundError:
        raise FileNotFoundError(
            "Config file not found. Please make sure guild-nfts_config.json exists.")


def get_all_nft_addresses(guild_id: str) -> List[str]:
    guild_config = get_config_for_guild(guild_id)
    if guild_config is None:
        return []
    else:
        return guild_config["addresses"]


def get_token_holder_role(guild_id: str) -> str:
    guild_config = get_config_for_guild(guild_id)
    if guild_config is None:
        raise Exception("Guild config not found")
    else:
        return guild_config["token_holder_role"]


def get_renting_role(guild_id: str) -> str:
    guild_config = get_config_for_guild(guild_id)
    if guild_config is None:
        raise Exception("Guild config not found")
    else:
        return guild_config["renting_role"]
