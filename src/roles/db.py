from tinydb import TinyDB, Query
from typing import List, Optional

db = TinyDB("db.json")

user_table = db.table("user")
guild_table = db.table("guild")

User = Query()
Guild = Query()


def get_all_guild_ids() -> List[str]:
    return list(map(lambda doc: doc["guild_id"], guild_table.all()))


def add_guild_id(guild_id: str):
    if not guild_table.contains(User.guild_id == guild_id):
        guild_table.insert({"guild_id": guild_id})


def add_user(guild_id: str, user_id: str, address: str):
    user_table.upsert(
        {"guild_id": guild_id, "user_id": user_id, "address": address},
        User.fragment({"guild_id": guild_id, "user_id": user_id}),
    )


def get_address(guild_id: str, user_id: str) -> Optional[str]:
    doc = user_table.search(User.fragment({"guild_id": guild_id, "user_id": user_id}))
    if doc == []:
        return None
    return doc[0]["address"]
