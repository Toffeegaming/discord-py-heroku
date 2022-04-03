import interactions, main

guilds = main.list_guild_ids

class Ping(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command(
        name='Ping',
        description='Pong!',
        scope=guilds
        )
    async def _Ping(self,ctx:  interactions.CommandContext):
        await ctx.send(f"Pong! ({self.client.latency*1000}ms)")

def setup(client: interactions.Client):
    Ping(client)
