import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand


import os

bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

async def PrintToLogChannel(message):
    print(message)
    logChannel = bot.get_channel(os.getenv("LOGS"))
    await logChannel.message.send(message)

@bot.event 
async def on_ready():
    await PrintToLogChannel(f"Logged in as {bot.user.name}({bot.user.id})")
    await bot.change_presence(activity=discord.Game(name='with my feelings'),status=discord.Status.online)

async def load_cogs():
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for filename in os.listdir(dir_path + '/cogs'):
        if filename.endswith('.py'):
            bot.load_extension(f'cogs.{filename[:-3]}')
            await PrintToLogChannel(f"[COGS] loaded {filename[:-3]}")
        else:
            await PrintToLogChannel(f'[COGS] Unable to load {filename[:-3]}')

# load cogs
await load_cogs()

# Create bot
bot.run(os.getenv("DISCORD_TOKEN"))
