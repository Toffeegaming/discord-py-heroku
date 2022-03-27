import interactions

class Say(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client

    @interactions.extension_command(name='Say', description='Zeg shit', scope=[477506300947857418]
        # , options=[
        #     create_option(
        #             name="text",
        #             description="What to repeat",
        #             option_type=3,
        #             required=False
        #         )
        # ]
        )
    async def _Say(self,ctx: interactions.CommandContext):
        await ctx.send(f"Out of order")

def setup(client: interactions.Client):
    Say(client)