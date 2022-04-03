import interactions

class Ping(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command(
        name='ping',
        description='Pong!'
        )
    async def ping(self,ctx:  interactions.CommandContext):
        await ctx.send(f"Pong! ({self.client.latency}ms)")

def setup(client: interactions.Client):
    Ping(client)
