import discord
from discord.ext import commands
from config import cfg


class Wallet(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def verify(self, ctx: commands.Context):
        url = cfg["Settings"]["api_base_url"] + \
            cfg["Settings"]["api_port"] + \
            "/connect?userid=" + str(ctx.author.id)

        title = "Connect Your Wallet"
        body = f"To connect your wallet [click here]({url})."
        colour = int(cfg["Settings"]["colour"], 16)
        embed = discord.Embed(title=title, description=body, colour=colour)

        try:
            await ctx.author.send(embed=embed)
        except Exception:
            path = ("'Privacy Settings'" " -> "
                    "'Allow direct messages from server members.'")
            await ctx.send(("{} Please enable {} for this server "
                            "to verify your account.").format(
                ctx.author.mention, path))
            return
        await ctx.send(f"{ctx.author.mention} Please check DMs.")
