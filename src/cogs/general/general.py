import discord
from discord.ext import commands
from utils.utils import get_uptime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx: commands.Context):
        """Sends bot status"""
        await ctx.send(f"**Uptime**: {round(get_uptime(), 1)}s\n"
                       f"**Connected Servers**: {len(self.bot.guilds)}\n"
                       f"**Discord API Latency**: {round(self.bot.latency, 4)}s\n")
