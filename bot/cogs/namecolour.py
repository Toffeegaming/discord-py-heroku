import interactions
import os
import gspread


class Kleur(interactions.Extension):
    def __init__(self, client) -> None:
        self.client = client
        self.RoleData = self.CreateGspread()
        print(self.RoleData)

    def CreateGspread(self):
        credentials = {
            "type": "service_account",
            "project_id": str(os.getenv("G_API_ID")),
            "private_key_id": str(os.getenv("G_API_KEY_ID")),
            "private_key": str(os.getenv("G_API_KEY").replace('\\n', '\n')),
            "client_email": str(os.getenv("G_API_MAIL")),
            "client_id": str(os.getenv("G_API_C_ID")),
            "auth_uri": "https://accounts.google.com/o/oauth2/auth",
            "token_uri": "https://oauth2.googleapis.com/token",
            "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
            "client_x509_cert_url": str(os.getenv("G_API_CURL"))
        }

        gc = gspread.service_account_from_dict(credentials)
        sh = gc.open('DiscordUserdata')
        googleData = sh.worksheet("RoleData")

        List = []
        counter = int(googleData.acell('C1').value)

        for i in range(counter):
            List.append(int(googleData.acell(f'A{i+1}').value))
            List.append(int(googleData.acell(f'B{i+1}').value))
            print(i+1)

        return List

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
    async def kleur(self, ctx: interactions.CommandContext, input=''):
        hasHash = False
        has0X = False
        hexcode = ''

        if "0x" in input:
            hexcode = input.replace('0x', '#')
            has0X = True
            print("has 0x")
        if "#" in input:
            hexcode = input
            input = input.replace('#', '0x')
            hasHash = True
            print("has hash")

        if not has0X and not hasHash:
            errorKleur = "0xff0000"
            errorKleur = int(errorKleur, 16)
            textEmbed = interactions.Embed(
                title="",
                description="Geef een geldige code, beginnend met # of 0x.",
                color=errorKleur)
            await ctx.send(embeds=textEmbed)
        else:
            input.ljust(8)
            input = int(input, 16)

            try:
                user_id_index = int(self.RoleData.index(int(ctx.author.id)))
                user_role_id = self.RoleData[user_id_index + 1]
                await self.client._http.modify_guild_role(guild_id=ctx.guild_id, role_id=user_role_id, data={"color": input})

                textEmbed = interactions.Embed(
                    title="",
                    description=f"Kleur veranderd. {hexcode}",
                    color=input)
                await ctx.send(embeds=textEmbed)
            except ValueError:
                textEmbed = interactions.Embed(
                    title="",
                    description="Iets ging fout, probeer het later opnieuw",
                    color=input)
                await ctx.send(embeds=textEmbed)
                self.RoleData = self.CreateGspread()


def setup(client: interactions.Client):
    Kleur(client)
