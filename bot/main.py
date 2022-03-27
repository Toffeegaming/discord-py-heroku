import interactions, os, sys, datetime

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

intents = interactions.Intents.GUILD_MEMBERS | interactions.Intents.GUILD_MESSAGES | interactions.Intents.GUILD_MESSAGE_REACTIONS | interactions.Intents.DIRECT_MESSAGES | interactions.Intents.GUILDS
presence = interactions.PresenceActivity(name="with code", type=interactions.PresenceActivityType.GAME)


bot = interactions.Client(token=os.getenv("DISCORD_TOKEN"), intents=intents, presence=interactions.ClientPresence(activities=[presence]), disable_sync=False)

# bot = Bot(command_prefix=os.getenv("DISCORD_PREFIX"), help_command=None, description=os.getenv("DISCORD_DESCRIPTION"), intents=discord.Intents.all())
# slash = SlashCommand(bot, sync_commands=True)

global list_guild_ids
list_guild_ids = []

async def getNumberGuilds():
    guild_list = await bot._http.get_self_guilds()
    for guild in guild_list:
        list_guild_ids.append( int( guild.id ) )

@bot.event 
async def on_ready():
    print(f"Logged in as {bot.me.name}({bot.me.id})")
    channel = interactions.Channel(**await bot._http.get_channel( int( os.getenv("LOGS")) ), _client=bot._http)

    await getNumberGuilds()
    time = datetime.datetime.utcnow()
    await channel.send(f"[{time}] [STARTUP] Logged in in {len(list_guild_ids)} servers!{os.linesep}{list_guild_ids}")
    
    #await bot.change_presence(activity=discord.Game(name=f'in {len(list_guild_ids)} servers'),status=discord.Status.online)

# load cogs
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        print(f'[COGS] Unable to load {filename}')

# Create bot
bot.start()
