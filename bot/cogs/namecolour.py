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
            print("has hash")
        if "0x" in input:
            has0X = True
            print("has 0x")

        if not has0X and not hasHash:
            await ctx.send("Geef een geldige code, beginnend met # of 0x")
            print("invalid input")
        else:
            if hasHash:
                input.replace('#','0x')
            input.ljust(8)

            
            user_id_index = int( self.data.index( int( ctx.author.id) ) )
            print(user_id_index)
            user_role_id = self.data[user_id_index + 1]
            print(user_role_id)

 

            await self.client.http.modify_guild_role(guild_id=ctx.guild_id, role_id=user_role_id, data={"color": input})
            #currentGuild = await ctx.get_guild()
            #print("guild retrieved")
            #currentGuild = interactions.Guild(**await self.client._http.get_guild(956152709034164224, client = self.client._http) )

            
            
           # testRole = await ctx.guild.get_role(user_role_id)
            #await testRole.modify(color = input, reason="Deze persoon wilde een andere kleur")

            #roles = await currentGuild.get_all_roles()
            #for role in roles:
            #    if role.id == user_role_id:
            #        r = role
            #        break
            #    else:
            #        r = None
            #if r:
            #    await r.modify(color = input, reason="Deze persoon wilde een andere kleur")
            await ctx.send(f"Kleur veranderd in {input}")

def setup(client: interactions.Client):
    Kleur(client)
