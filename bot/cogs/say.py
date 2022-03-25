# from discord.ext.commands import Bot, Cog
# from discord_slash import cog_ext, SlashContext
# from discord_slash.utils.manage_commands import create_option

# class Say(Cog):
#     def __init__(self, bot: Bot):
#         self.bot = bot

#     @cog_ext.cog_slash(name='Say', description='Zeg shit', guild_ids=[477506300947857418],
#         options=[
#             create_option(
#                     name="text",
#                     description="What to repeat",
#                     option_type=3,
#                     required=False
#                 )
#         ])
#     async def _Say(self,ctx: SlashContext, text=None):
#         await ctx.send(f"[Phasmo locaties]({text})")

# def setup(bot: Bot):
#     bot.add_cog( Say(bot) )