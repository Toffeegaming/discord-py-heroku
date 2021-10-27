import os

from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

from mcstatus import MinecraftServer

MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

class Minecraft(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    @cog_ext.cog_slash( name='Server', description='Check of de minecraft server online is.', guild_ids = MCServer)
    async def _Server(self, ctx: SlashContext):
        decorator = "```"
        message = ""
        try:
            ip = os.getenv("SERVER")
            print(f"[MC] Got ip from env")

            server = MinecraftServer(ip,25565)

            latency = int(server.ping())
            print(f"[MC] Pinged server")

            if latency > 5:
                print(f"[MC] Server Online")
                query = server.query()
                print(f"[MC] Server queried")

                placeholder = "{names}"
                test = placeholder.format( names = "\n".join(query.players.names) )
                if test:
                    names = "Deze mensen zijn op de server:\n" + test
                    print(f"[MC] People online")
                else:
                    names = "Niemand is online"
                    print(f"[MC] Nobody online")

                intro = "De server is online!\n"
                message = intro + names
                print(f"[MC] Message set with active members")
            else:
                print(f"[MC] Server offline")
                message = "Server is offline"

        except:
            print(f"[MC] Exception triggered")
            message = "Server is offline"
            await ctx.send(decorator + message + decorator)

        else:
            print(f"[MC] Else triggered")
            message = "Server is offline"

        await ctx.send(decorator + message + decorator)
        print(f"[MC] Message sent")


def setup(bot: Bot):
    bot.add_cog( Minecraft(bot) )
