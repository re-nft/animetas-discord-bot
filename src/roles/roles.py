import discord
from dataclasses import dataclass
from discord.utils import get
from config import cfg
from typing import List, Optional
from utils.utils import get_guild, get_member
from .animetas import verify_wallet_has_any_valid_token
from .renft import verify_address_currently_rents_configured_nfts


def get_roles_to_assign(address: str) -> List[str]:
    roles = set()
    if verify_wallet_has_any_valid_token(address):
        roles.add(cfg["Settings"]["token_holder_role"])
    if verify_address_currently_rents_configured_nfts(address):
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
    roles: List[discord.Role]


def get_discord_user(guild_id: str, user_id: str, address: str) -> DiscordUser:
    _guild: Optional[discord.Guild] = get_guild(guild_id)
    if _guild is None:
        raise Exception("Guild does not exist.")
    guild: discord.Guild = _guild

    _member: Optional[discord.Member] = get_member(user_id, guild)
    if _member is None:
        raise Exception("Member does not exist in guild.")
    member: discord.Member = _member

    def get_role(role_name: str) -> discord.Role:
        role: Optional[discord.Role] = get(guild.roles, name=role)
        if role is None:
            raise Exception(f"Role {role_name} does not exist.")
        return role

    roles = get_roles_to_assign(address)
    discord_roles: List[discord.Role] = []

    if len(roles) > 0:
        discord_roles = list(
            map(lambda role_name: get_role(role_name), roles))

    return DiscordUser(guild, member, discord_roles)
