import discord
from discord.ext import commands
from config import cfg
from utils.utils import send_embed_dm


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx: commands.Context):
        url = cfg["Settings"]["api_base_url"] + \
            ":" + \
            cfg["Settings"]["public_api_port"] + \
            "/connect?userid=" + str(ctx.author.id) + \
            "&guildid="+str(ctx.guild.id)

        title = "Connect Your Wallet"
        body = f"To connect your wallet [click here]({url})."
        colour = int(cfg["Settings"]["colour"], 16)
        embed = discord.Embed(title=title, description=body, colour=colour)

        try:
            await send_embed_dm(ctx.author, embed, ctx)
            await ctx.send(f"{ctx.author.mention} Please check DMs.")
        except Exception:
            pass
