import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

class Ping(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.guild_ids = _getGuilds()
    
    def _getGuilds(self):
        list = []
        for guild in self.bot.guilds:
            list.append(guild.id)
        print(list)
        return list

    @cog_ext.cog_slash(name='Ping', description='Pong!', guild_ids=self.guild_ids)
    async def _Ping(self,ctx: SlashContext):
        await ctx.send(f"Pong! ({self.bot.latency*1000}ms)")

def setup(bot: Bot):
    bot.add_cog( Ping(bot) )
