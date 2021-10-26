#import discord
from discord_slash import SlashCommand, cog_ext, SlashContext
from mcstatus import MinecraftServer

class Minecraft(commands.Cog)
    def __init__(self, bot):
        self.bot = bot
    
    MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

    @cog_ext.cog_slash(
    name='Server',
    description='Check of de minecraft server online is.',
    guild_ids = MCServer)
    async def _Server(ctx):
        print(f"Started running server command")
        try:
            ip = os.getenv("SERVER")
            server = MinecraftServer(ip,25565)
            query = server.query()
            placeholder = "{names}"
            test = placeholder.format( names = ", ".join(query.players.names) )
            if test:
                names = "Deze mensen zijn op de server: " + test
            else:
                names = "Niemand is online"
            intro = "De server is online!\n"
            message = intro + names
            await ctx.send( message )

        except:
            await ctx.send("Server is offline")

def setup(bot):
    bot.add_cog( Minecraft(bot) )
