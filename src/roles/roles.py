import discord
from config import cfg
from typing import List
from .animetas import verify_wallet_has_any_valid_token
from .renft import verify_address_has_animetas_nft


def get_roles_to_assign(address: str) -> List[str]:
    roles = set()
    if verify_wallet_has_any_valid_token(address):
        roles.add(cfg["Settings"]["token_holder_role"])
    if verify_address_has_animetas_nft(address):
        roles.add(cfg["Settings"]["renting_role"])
    return list(roles)


async def assign_roles(member: discord.Member, roles: List[discord.Role]):
    await member.add_roles(*roles)
