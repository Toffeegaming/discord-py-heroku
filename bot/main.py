import discord
from discord.ext import commands

from discord_slash import SlashCommand
from discord_slash.utils.manage_commands import create_option

from datetime import datetime

import os

TOKEN = os.getenv("DISCORD_TOKEN")
OWNER = os.getenv("OWNER")


guild_ids = [ int(os.getenv("GUILD1")), int(os.getenv("GUILD2")), int(os.getenv("GUILD3")) ]

bot = commands.Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event # ready messages
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    print()
    await bot.change_presence(activity=discord.Game(name='with my feelings'),status=discord.Status.online)
    owner = await bot.fetch_user(OWNER)
    rawtime = datetime.now()
    formatTime = rawtime.strftime("%d-%b-%Y (%H:%M:%S)")
    await owner.send('Bot is online @' + formatTime)


@bot.event # error handler
async def on_slash_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        await ctx.send("That command wasn't found! Sorry :(")
    if isinstance(error, discord.HTTPException):
        await ctx.send("You cannot bonk them!")

@slash.slash(
    name='Ping',
    description='Pong!',
    guild_ids=guild_ids)
async def _Ping(ctx):
    await ctx.send(f"Pong! ({bot.latency*1000}ms)")

@slash.slash(
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
        await target.send(sender +" finds you shameful!\nhttps://tenor.com/view/shame-go-t-game-of-thrones-walk-of-shame-shameful-gif-4949558")
        await ctx.send("Shame has been delivered!")


@slash.slash(
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



@slash.slash(
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

#Create bot
bot.run(TOKEN)