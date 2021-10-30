import discord
from discord.ext.commands import Bot
from discord_slash import SlashCommand


import os

bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
slash = SlashCommand(bot, sync_commands=True)

@bot.event 
async def on_ready():
    message = f"Logged in as {bot.user.name}({bot.user.id})"
    print(message)
    logChannel = bot.get_channel(os.getenv("LOGS"))
    await logChannel.send(message)
    await bot.change_presence(activity=discord.Game(name='with my feelings'),status=discord.Status.online)


# load cogs
dir_path = os.path.dirname(os.path.realpath(__file__))
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        print(f'[COGS] Unable to load {filename[:-3]}')



# Create bot
bot.run(os.getenv("DISCORD_TOKEN"))
