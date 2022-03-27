import os
import discord

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

from discord_slash.utils.manage_commands import create_option

guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

class Shame(Cog):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command( name='Shame', description='Shame those who deserve it', guild_ids=guild_ids,
        options=[
            create_option(
                    name="target",
                    description="Who needs to be publicly shamed?",
                    option_type=6,
                    required=False)] )
    async def _Shame(self,ctx: interactions.CommandContext, victim=None):
        if victim is None:
            await ctx.send("https://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
        else:
            await ctx.send("This is currently under construction")

            # # TODO: make embed
            # sender = ctx.author.name
            # target = await self.bot.fetch_user(victim.id)
            # await target.send("You got shamed by " + sender +"!\nhttps://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
            # await ctx.send("Shame has been delivered!")

    @_Shame.error # error handler
    async def _Shame_error(self, ctx, error):
        await ctx.send("ERROR!")
        if isinstance(error, discord.HTTPException):
            await ctx.send("You cannot send a DM to this person.")

def setup(bot: Bot):
    bot.add_cog( Shame(bot) )