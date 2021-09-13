from discord.ext import commands
from utils.utils import get_uptime


class General(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def status(self, ctx: commands.Context):
        """Sends bot status"""
        msg = ("**Uptime**: {}s\n"
               "**Connected Servers**: {} server(s)\n"
               "**Discord API Latency**: {}s").format(
            round(get_uptime(), 1),
            len(self.bot.guilds),
            round(self.bot.latency, 4))
        await ctx.send(msg)
