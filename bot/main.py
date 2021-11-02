import os
import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand
from discord.utils import get

import datetime # timestamp discord log output

bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event 
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    time = datetime.datetime.utcnow()
    await bot.get_channel( int(os.getenv("LOGS")) ).send(f"[{time}] [STARTUP] Logged in!")
    await bot.change_presence(activity=discord.Game(name='with my feelings'),status=discord.Status.online)

    user = get(bot.get_all_members(), id="228537642583588864")
    if user:
        # found the user
        await user.edit(nick='Shelly')

# load cogs
dir_path = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        if filename != 'jsonfiles':
            print(f'[COGS] Unable to load {filename[:-3]}')

# Create bot
bot.run(os.getenv("DISCORD_TOKEN"))
