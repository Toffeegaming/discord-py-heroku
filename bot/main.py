import discord

from discord.ext.commands import Bot

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

import os

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER = os.getenv("OWNER")

guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

# Load cogs
def LoadCogs():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(dir_path + '/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            print(f"[COGS] loaded {filename[:-3]}")
        else:
            print(f'[COGS] Unable to load {filename[:-3]}')

@bot.event 
async def on_ready():
    LoadCogs()
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name='with my feelings'),status=discord.Status.online)
    owner = await bot.fetch_user(OWNER)


@bot.event # error handler
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")
    if isinstance(error, discord.HTTPException):
        await ctx.send("You cannot that action")


@slash.slash( #ping
    name='Ping',
    description='Pong!',
    guild_ids=guild_ids)
async def _Ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

@slash.slash( #shame
    name='Shame',
    description='Shame those who deserve it',
    options=[
        create_option(
                 name="target",
                 description="Who needs to be publicly shamed?",
                 option_type=6,
                 required=False
               )
    ],
    guild_ids=guild_ids)
async def _Shame(ctx, victim=None):
    if victim is None:
        await ctx.send("https://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
    else:
        # TODO: make embed
        sender = ctx.author.name
        target = await bot.fetch_user(victim.id)
        await target.send("You got shamed by " + sender +"!\nhttps://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
        await ctx.send("Shame has been delivered!")

@slash.slash( #bonk
    name='Bonk',
    description='Bonk the horny people',
    options=[
        create_option(
                 name="victim",
                 description="Who is horny?",
                 option_type=6,
                 required=False
               )
    ],
    guild_ids=guild_ids)
async def _Bonk(ctx, victim=None):
    if victim is None:
        await ctx.send("https://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755")
    else:
        # TODO: make embed
        sender = ctx.author.name
        target = await bot.fetch_user(victim.id)
        await target.send("You got bonked by " + sender +"!\nhttps://tenor.com/view/horny-jail-bonk-dog-hit-head-stop-being-horny-gif-17298755")
        await ctx.send("BONK!")

@slash.slash( # geil
    name='Geil',
    description='Horny or normie?',
    guild_ids=guild_ids)
async def _Geil(ctx):
    id = ctx.author_id
    mention = ctx.author.mention
    if id == os.getenv("BEAST"):
        await ctx.send(mention + " is de geilste persoon in Nederland")
    if id == os.getenv("CUTIE"):
        await ctx.send(mention + " is een cutie :)")
    else:
        await ctx.send(mention + " is een sexy beast")


# from mcstatus import MinecraftServer

# MCServer = [int(os.getenv("GUILD2")),int(os.getenv("GUILD3"))]

# @slash.slash( #server status
#     name='Server',
#     description='Check of de minecraft server online is.',
#     guild_ids = MCServer)
# async def _Server(ctx):
#     print(f"Started running server command")
#     try:
#         ip = os.getenv("SERVER")
#         server = MinecraftServer(ip,25565)
#         query = server.query()
#         placeholder = "{names}"
#         test = placeholder.format( names = ", ".join(query.players.names) )
#         if test:
#             names = "Deze mensen zijn op de server: " + test
#         else:
#             names = "Niemand is online"
#         intro = "De server is online!\n"
#         message = intro + names
#         await ctx.send( message )

#     except:
#         await ctx.send("Server is offline")

# Create bot
bot.run(TOKEN)
