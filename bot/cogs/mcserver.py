# import main

# from discord.ext.commands import Bot, Cog
# from discord_slash import cog_ext, SlashContext
# from mcstatus import MinecraftServer

# guild_ids=main.list_guild_ids

# class Minecraft(Cog):
#     def __init__(self, bot: Bot):
#         self.bot = bot

#     @cog_ext.cog_slash( name='Server', description='Check of de minecraft server online is.', guild_ids = guild_ids)
#     async def _Server(self, ctx: SlashContext):
#         decorator = "```"
#         message = ""
#         try:
#             ip = os.getenv("SERVER")
#             print(f"[MC] Got ip from env")

#             server = MinecraftServer(ip,25565)

#             query = server.query()
#             print(f"[MC] Server queried")

#             placeholder = "{names}"
#             test = placeholder.format( names = "\n".join(query.players.names) )
#             if test:
#                 names = "Deze mensen zijn op de server:\n" + test
#                 print(f"[MC] People online")
#             else:
#                 names = "Niemand is online"
#                 print(f"[MC] Nobody online")

#             intro = "De server (toffeegaming.ddns.net) is online!\n"
#             message = intro + names
#             print(f"[MC] Message set with active members")

#             await ctx.send(decorator + message + decorator ,delete_after=120)
#             print(f"[MC] Message sent | Online")

#         except:
#             print(f"[MC] Exception triggered")
#             await ctx.send("```Server toffeegaming.ddns.net is offline```",delete_after=120)

#     @_Server.error # error handler
#     async def _Server_error(self, ctx, error):
#         print(f"[MC] Exception handler triggered")
#         await ctx.send("```Server toffeegaming.ddns.net is offline```",delete_after=120)


# def setup(bot: Bot):
#     bot.add_cog( Minecraft(bot) )