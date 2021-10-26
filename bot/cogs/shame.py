import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

class Shame(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash( name='Shame', description='Shame those who deserve it', guild_ids=guild_ids,
        options=[
            create_option(
                    name="target",
                    description="Who needs to be publicly shamed?",
                    option_type=6,
                    required=False)] )
    async def _Shame(ctx, victim=None):
        if victim is None:
            await ctx.send("https://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
        else:
            await ctx.send("This is currently under construction")

            # # TODO: make embed
            # sender = ctx.author.name
            # target = await bot.fetch_user(victim.id)
            # await target.send("You got shamed by " + sender +"!\nhttps://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
            # await ctx.send("Shame has been delivered!")

def setup(bot: Bot):
    bot.add_cog( Shame(bot) )