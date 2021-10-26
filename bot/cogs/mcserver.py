import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

from mcstatus import MinecraftServer

MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

class Minecraft(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        print(f"[MC] Cog initialised")

    @cog_ext.cog_slash( name='Server', description='Check of de minecraft server online is.', guild_ids = MCServer)
    async def _Server(self, ctx: SlashContext):
        print(f"Started running server command")
        try:
            ip = os.getenv("SERVER")
            print(f"[MC] Got IP")

            server = MinecraftServer(ip,25565)
            print(f"[MC] Got server")

            query = server.query()
            print(f"[MC] Query succes")

            placeholder = "{names}"
            test = placeholder.format( names = ", ".join(query.players.names) )
            if test:
                names = "Deze mensen zijn op de server: " + test
                print(f"[MC] People on server")
            else:
                names = "Niemand is online"
                print(f"[MC] Server empty")

            intro = "De server is online!\n"
            message = intro + names
            await ctx.send( message )
            print(f"[MC] Responded")

        except:
            await ctx.send("Server is offline")
            print(f"[MC] Responded")

def setup(bot: Bot):
    bot.add_cog( Minecraft(bot) )

# from mcstatus import MinecraftServer

# MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

# @slash.slash( #server status
#     name='Server',
#     description='Check of de minecraft server online is.',
#     guild_ids = MCServer)
# async def _Server(ctx):
#     print(f"Started running server command")
#     try:
#         ip = os.getenv("SERVER")
#         server = MinecraftServer(ip,25565)
#         query = server.query()
#         placeholder = "{names}"
#         test = placeholder.format( names = ", ".join(query.players.names) )
#         if test:
#             names = "Deze mensen zijn op de server: " + test
#         else:
#             names = "Niemand is online"
#         intro = "De server is online!\n"
#         message = intro + names
#         await ctx.send( message )

#     except:
#         await ctx.send("Server is offline")
