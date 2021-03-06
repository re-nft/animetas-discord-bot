from discord import HTTPException
from utils.utils import set_start_time, get_uptime, shutdown
from utils.logger import add_handlers, logger
from client import client as bot
from api import app
from env import set_env_file
import cogs
import signal
import os
import time
import asyncio
import argparse
import dotenv

parser = argparse.ArgumentParser()
parser.add_argument(
    "--env-file", help="environment variable file to use", default=".env"
)
args = parser.parse_args()

env_file = args.env_file
set_env_file(env_file)
dotenv.load_dotenv(env_file)
add_handlers()


set_start_time(time.perf_counter())

for cog in cogs.cogs:
    bot.add_cog(cog(bot))


@bot.event
async def on_connect():
    """
    Connected to Discord
    """
    logger.info(f"{bot.user} is online, logged into {len(bot.guilds)} server(s).")


@bot.event
async def on_ready():
    logger.info(
        "Server List:\n"
        + "\n".join(
            f"\t{server.name} " f"({len(server.members)} members)"
            for server in bot.guilds
        )
    )

    logger.info(f"Startup completed in {round(get_uptime(),3)}s")


# TODO: Fix killing the bot
signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
for s in signals:
    bot.loop.add_signal_handler(
        s, lambda s=s: asyncio.create_task(shutdown(s, bot.loop))
    )
port = int(os.getenv("LOCAL_API_PORT", "5000"))

discord_bot_enabled = os.getenv("DISCORD_BOT_ENABLED", "True").lower() in (
    "true",
    "1",
    "t",
)
web_server_enabled = os.getenv("WEB_SERVER_ENABLED", "True").lower() in (
    "true",
    "1",
    "t",
)

try:
    if web_server_enabled and discord_bot_enabled:
        bot.loop.create_task(
            app.run_task(
                host="0.0.0.0",
                port=port,
                certfile=os.getenv("CERT_FILE"),
                keyfile=os.getenv("KEY_FILE"),
            )
        )
        bot.run(os.environ.get("TOKEN"))
    elif web_server_enabled and not discord_bot_enabled:
        app.run(
            host="0.0.0.0",
            port=port,
            certfile=os.getenv("CERT_FILE"),
            keyfile=os.getenv("KEY_FILE"),
        )
    elif not web_server_enabled and discord_bot_enabled:
        bot.run(os.environ.get("TOKEN"))
except HTTPException:
    # restart on HTTP 429 Too Many Requests
    os.system("kill 1")
except KeyboardInterrupt:
    logger.info("Process interrupted")
finally:
    if discord_bot_enabled:
        bot.loop.close()
    logger.info("Successfuly shutdown reNFT Discord service")
