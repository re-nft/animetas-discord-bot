import os
import discord
from discord.ext import commands
import dotenv
from config import cfg
from utils.utils import send_embed_dm
from env import get_env_file


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def renft(self, ctx: commands.Context):
        dotenv.load_dotenv(get_env_file())

        base_url = os.getenv("PUBLIC_API_BASE_URL", "http://localhost")
        port = os.getenv("PUBLIC_API_PORT", "5000")

        url = (
            base_url
            + ":"
            + port
            + "/connect?userid="
            + str(ctx.author.id)
            + "&guildid="
            + str(ctx.guild.id)
        )

        title = "Connect Your Wallet"
        body = f"To connect your wallet [click here]({url})."
        colour = int(cfg["Settings"]["colour"], 16)
        embed = discord.Embed(title=title, description=body, colour=colour)

        try:
            await send_embed_dm(ctx.author, embed, ctx)
            await ctx.send(f"{ctx.author.mention} Please check DMs.")
        except Exception:
            pass
