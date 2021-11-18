import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from main import list_guild_ids

class Ping(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name='Ping', description='Pong!', guild_ids=list_guild_ids)
    async def _Ping(self,ctx: SlashContext):
        await ctx.send(f"Pong! ({self.bot.latency*1000}ms)")

def setup(bot: Bot):
    bot.add_cog( Ping(bot) )
