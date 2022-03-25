import string
from typing import Hashable
import interactions

class Kleur(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client
    
    # person id - role id
    data = [
        126674618575618048, 956172644481368064,
        318770388374913025, 956206878063489075,
        193690170669793280, 956206814146482246,
        193416532125155329, 956206857108725860,
        277129696469188620, 956206897558593626,
        294031838291296258, 956206986679160904,
        199147443722518528, 956206917942935602
    ]

    @interactions.extension_command(
        name='kleur',
        description='Verander de kleur van je nickname',
        scope=956152709034164224,
        options=[
            interactions.Option(
                    name="input",
                    description="Hex code van de kleur die je wilt",
                    type=interactions.OptionType.STRING,
                    required=False,
                ),
        ],
    )
    async def kleur(self,ctx: interactions.CommandContext, input:string = '0x000000'):
        hasHash = False
        has0X = False
        
        if "#" in input:
            hasHash = True
        if "0x" in input:
            has0X = True

        if not has0X and not hasHash:
            await ctx.send("Geef een geldige code, beginnend met # of 0x")
        else:
            if hasHash:
                input.replace('#','0x')
            input.ljust(8)

            currentGuild = interactions.Guild(**await self.client._http.get_guild(956152709034164224))

            user_role_id = self.data[ int(self.data.index(ctx.author.id) ) + 1]

            await currentGuild.modify_role(role_id=user_role_id, color = input, reason="Deze persoon wilde een andere kleur")
            await ctx.send(f"Kleur veranderd in {input}")

def setup(client: interactions.Client):
    Kleur(client)
