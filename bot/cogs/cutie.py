import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

class Cutie(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash( name='Cute', description='Hoe cute ben je?', guild_ids=guild_ids)
    async def _Cute(self,ctx):
        id = ctx.author_id
        mention = ctx.author.mention
        if id == os.getenv("BEAST"):
            await ctx.send(mention + " is de geilste persoon in Nederland")
        if id == os.getenv("CUTIE"):
            await ctx.send(mention + " is de beste cutie van Nederland :)")
        else:
            await ctx.send(mention + " is een cute")

def setup(bot: Bot):
    bot.add_cog( Cutie(bot) )
