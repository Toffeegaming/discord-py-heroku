import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

class Bonk(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash( name='Bonk', description='Bonk the horny people', guild_ids=guild_ids,
        options=[
            create_option(
                    name="victim",
                    description="Who is horny?",
                    option_type=6,
                    required=False
                )
        ])
    async def _Bonk(ctx, victim=None):
        if victim is None:
            await ctx.send("https://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755")
        else:
            # TODO: make embed
            sender = ctx.author.name
            target = await bot.fetch_user(victim.id)
            await target.send("You got bonked by " + sender +"!\nhttps://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755")
            await ctx.send("BONK!")

def setup(bot: Bot):
    bot.add_cog( Bonk(bot) )