import time
import dotenv
import os

import cogs
from client import client as bot
from utils.logger import logger
from utils.utils import set_start_time, get_uptime

from discord import HTTPException


dotenv.load_dotenv()
set_start_time(time.perf_counter())

for cog in cogs.cogs:
    bot.add_cog(cog(bot))


@bot.event
async def on_connect():
    '''
    Connected to Discord
    '''
    logger.info(
        f"{bot.user} is online, logged into {len(bot.guilds)} server(s).")


@bot.event
async def on_ready():
    logger.info("Server List:\n" +
                "\n".join(
                    f"\t{server.name} "
                    f"({len(server.members)} members)"
                    for server in bot.guilds))

    logger.info(f"Startup completed in {round(get_uptime(),3)}s")

try:
    bot.run(os.environ.get("TOKEN"))
except HTTPException:
    # restart on HTTP 429 Too Many Requests
    os.system("kill 1")
