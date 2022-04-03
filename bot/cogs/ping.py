import interactions, os, sys

sys.path.append(os.getcwd())
from main import list_guild_ids

class Ping(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command(
        name='Ping',
        description='Pong!',
        scope=list_guild_ids
        )
    async def _Ping(self,ctx:  interactions.CommandContext):
        await ctx.send(f"Pong! ({self.client.latency*1000}ms)")

def setup(client: interactions.Client):
    Ping(client)
