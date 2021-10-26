import os

from mcstatus import MinecraftServer

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

class Minecraft(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
    MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

    @cog_ext.cog_slash(
    name='Server',
    description='Check of de minecraft server online is.',
    guild_ids = MCServer)
    async def _Server(ctx: SlashContext):
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
