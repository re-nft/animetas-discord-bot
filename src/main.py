import asyncio
import time
import dotenv
import os
import signal

import cogs
from api import app
from client import client as bot
from config import cfg
from utils.logger import logger
from utils.utils import set_start_time, get_uptime, shutdown

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

# TODO: Fix killing the bot
signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
for s in signals:
    bot.loop.add_signal_handler(
        s, lambda s=s: asyncio.create_task(shutdown(s, bot.loop)))

try:
    bot.loop.create_task(app.run_task(
        host="0.0.0.0", port=int(cfg["Settings"]["api_port"])))
    bot.run(os.environ.get("TOKEN"))
except HTTPException:
    # restart on HTTP 429 Too Many Requests
    os.system("kill 1")
except KeyboardInterrupt:
    logger.info("Process interrupted")
finally:
    bot.loop.close()
    logger.info("Successfuly shutdown reNFT Animetas service")
