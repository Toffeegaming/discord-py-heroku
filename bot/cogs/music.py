import os
#import discord

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

class Repeat(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash(name='Repeat', description='make me say stuff!', guild_ids=guild_ids)
    async def _Repeat(self,ctx: SlashContext, text=None):
        await ctx.send("+queue")

def setup(bot: Bot):
    bot.add_cog( Repeat(bot) )