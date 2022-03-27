import interactions, main

#guild_ids = main.list_guild_ids
guild_ids = [956152709034164224, 831642131986776125, 477506300947857418]

class Ping(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command(
        name='ping',
        description='Pong!',
        scope=guild_ids
        )
    async def ping(self,ctx:  interactions.CommandContext):
        await ctx.send(f"Pong! ({self.client.latency*1000}ms)")

def setup(client: interactions.Client):
    Ping(client)
