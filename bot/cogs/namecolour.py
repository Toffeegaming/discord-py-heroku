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
        199147443722518528, 956206917942935602,
        323712598036054018, 957568188269350962,
        243371926993633280, 958034959862476860
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
                    required=True,
                ),
        ],
    )
    async def kleur(self,ctx: interactions.CommandContext, input=''):
        hasHash = False
        has0X = False
        hexcode = ''
        if "#" in input:
            hexcode = input
            input = input.replace('#','0x')
            hasHash = True
            print("has hash")
        if "0x" in input:
            hexcode = input.replace('0x','#')
            has0X = True
            print("has 0x")
        if not has0X and not hasHash:
            errorKleur = "0xff0000"
            errorKleur = int(errorKleur, 16)
            textEmbed = interactions.Embed(
                title=f"",
                description=f"Geef een geldige code, beginnend met # of 0x.",
                color=errorKleur)
            await ctx.send(embeds=textEmbed)
        else:
            input.ljust(8)
            user_id_index = int( self.data.index( int( ctx.author.id) ) )
            user_role_id = self.data[user_id_index + 1]
            input = int(input, 16)
            await self.client._http.modify_guild_role(guild_id=ctx.guild_id, role_id=user_role_id, data={"color": input})
            textEmbed = interactions.Embed(
                title=f"",
                description=f"Kleur veranderd. {hexcode}",
                color=input)
            await ctx.send(embeds=textEmbed)

def setup(client: interactions.Client):
    Kleur(client)
