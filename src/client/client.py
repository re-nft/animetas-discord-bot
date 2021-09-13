import discord
from discord.ext import commands
from config import cfg
from utils.logger import logger
import time
import os

prefix = "!"
if cfg["Settings"]["prefix"]:
    prefix = cfg["Settings"]["prefix"]

intents = discord.Intents.all()

client = commands.Bot(
    command_prefix=prefix,
    case_insensitive=True,
    help_command=commands.DefaultHelpCommand(),
    intents=intents,
    status=discord.Status.online,
    activity=discord.Game(cfg["Settings"]["status"]))


@client.event
async def on_error(event, *args, **kwargs):
    try:
        raise Exception(event)
    except discord.HTTPException:
        # restart on HTTP 429 Too Many Requests
        os.system("kill 1")
    except Exception:
        logger.exception(event)


@client.event
async def on_command_error(ctx: commands.Context, exception):
    await ctx.send(f"Error: {exception}", reference=ctx.message)
    logger.exception("Command Error", exc_info=exception)


@client.before_invoke
async def set_before_command(ctx: commands.Context):
    ctx.invoke_time = time.perf_counter()


@client.after_invoke
async def log_after_command(ctx: commands.Context):
    time_taken_ms = (time.perf_counter() - ctx.invoke_time)*1000
    logger.debug(
        "Invoked command {} in ({} ms) at {}".format(
            ctx.command,
            round(time_taken_ms, 2),
            ctx.message.jump_url))
