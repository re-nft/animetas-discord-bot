import discord
from dataclasses import dataclass
from discord.utils import get
from discord.ext.tasks import loop
from config import cfg
from typing import List, Optional
from utils.utils import get_guild, get_member
from utils.logger import logger
from .nfts import verify_wallet_has_any_valid_token
from .renft import verify_address_currently_rents_configured_nfts
from roles.db import get_all_guild_ids, get_address


def get_roles_to_assign(address: str, guild_id: str) -> List[str]:
    roles = set()
    if verify_wallet_has_any_valid_token(address, guild_id):
        roles.add(cfg["Settings"]["token_holder_role"])
    if verify_address_currently_rents_configured_nfts(address, guild_id):
        roles.add(cfg["Settings"]["renting_role"])
    return list(roles)


async def assign_roles(member: discord.Member, roles: List[discord.Role]):
    await member.add_roles(*roles)


async def unassign_roles(member: discord.Member, roles: List[discord.Role]):
    await member.remove_roles(*roles)


@dataclass(frozen=True)
class DiscordUser:
    guild: discord.Guild
    member: discord.Member
    proposed_roles: List[discord.Role]


def get_role(guild: discord.Guild, role_name: str) -> discord.Role:
    role: Optional[discord.Role] = get(guild.roles, name=role_name)
    if role is None:
        raise Exception(f"Role {role_name} does not exist.")
    return role


def get_discord_user(guild_id: str, user_id: str, address: str) -> DiscordUser:
    _guild: Optional[discord.Guild] = get_guild(guild_id)
    if _guild is None:
        raise Exception("Guild does not exist.")
    guild: discord.Guild = _guild

    _member: Optional[discord.Member] = get_member(user_id, guild)
    if _member is None:
        raise Exception("Member does not exist in guild.")
    member: discord.Member = _member

    roles = get_roles_to_assign(address, guild_id)
    discord_roles: List[discord.Role] = []

    if len(roles) > 0:
        discord_roles = list(map(lambda role_name: get_role(guild, role_name), roles))

    return DiscordUser(guild, member, discord_roles)


@loop(hours=1)
async def check_roles_hourly():
    role_names = {
        cfg["Settings"]["token_holder_role"]: verify_wallet_has_any_valid_token,
        cfg["Settings"]["renting_role"]: verify_address_currently_rents_configured_nfts,
    }
    guild_ids = get_all_guild_ids()
    for guild_id in guild_ids:
        for role_name in role_names.keys():
            fn = role_names[role_name]
            try:
                _guild: Optional[discord.Guild] = get_guild(guild_id)
                if _guild is None:
                    raise Exception("Guild does not exist.")
                guild: discord.Guild = _guild
                role = get_role(guild, role_name)
                for member in role.members:
                    address = get_address(guild_id, str(member.id))
                    if address is None:
                        await unassign_roles(member, [role])
                        print(
                            (
                                f"Address is None for {member.name} "
                                f"with guild id {guild_id} "
                                f"and user_id {str(member.id)}"
                            )
                        )
                    elif not fn(address):
                        await unassign_roles(member, [role])

            except Exception as e:
                logger.exception(e)


check_roles_hourly.start()
