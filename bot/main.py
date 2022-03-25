# import discord, os, sys, datetime
# from discord.ext.commands import Bot
# from discord_slash import SlashCommand

import interactions, os, sys, datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

bot = interactions.Client(token=os.getenv("DISCORD_TOKEN"))

# bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
# slash = SlashCommand(bot, sync_commands=True)

global list_guild_ids
list_guild_ids = []

def getNumberGuilds():
    for guild in bot.guilds:
        list_guild_ids.append(guild.id)

@bot.event 
async def on_ready():
    print(f"Logged in as {bot.user.name}({bot.user.id})")
    time = datetime.datetime.utcnow()
    getNumberGuilds()
    await bot.get_channel( int(os.getenv("LOGS")) ).send(f"[{time}] [STARTUP] Logged in in {len(list_guild_ids)} servers!{os.linesep}{list_guild_ids}")
    #await bot.change_presence(activity=discord.Game(name=f'in {len(list_guild_ids)} servers'),status=discord.Status.online)

# load cogs
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load(name=f'cogs.{filename[:-3]}')
        #bot.load_extension(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        print(f'[COGS] Unable to load {filename}')

# Create bot
bot.start()
#bot.run(os.getenv("DISCORD_TOKEN"))