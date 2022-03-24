from os import getuid
from xmlrpc import client
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext
from discord_slash.utils.manage_commands import create_option
from discord.utils import get

test = 477506300947857418
live = 956152709034164224
guild_ids = [test]

class Kleur(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
    
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

    @cog_ext.cog_slash(name='Kleur', description='Verander de kleur van je nickname', guild_ids=guild_ids,
        options=[
            create_option(
                    name="input",
                    description="Hex code van de kleur die je wilt",
                    option_type=4,
                    required=True
                )
        ])
    async def _Kleur(self,ctx: SlashContext, input=None):
        user_role_id = self.data.index(ctx.author_id) + 1


        role = get(ctx.guild.roles, id=user_role_id)

        # guild = self.bot.get_guild(ctx.guild_id)
        # for role in guild.roles:
        #     if role.id == user_role_id:
        #         await self.bot.
        # role = ctx.guild.get_role(user_role_id)

        await role.edit(color=input, reason="Deze persoon wilde een andere kleur")
        await ctx.send("Kleur veranderd!")

def setup(bot: Bot):
    bot.add_cog( Kleur(bot) )