import interactions, os, sys, datetime, gspread, json

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)


def get_data(name):
    file_location = dir_path + '/cogs/' + name + '.json'
    with open(file_location, 'r') as file:
        return json.loads(file.read())

def set_data(data,name):
    file_location = dir_path + '/cogs/' + name + '.json'
    with open(file_location, 'w') as file:
        file.write(json.dumps(data, indent=2))

def CreateGspread():
    g_file = 'jsonfiles/google_api_secret'
    data = get_data(g_file)
    data['project_id'] = os.getenv("G_API_ID")
    data['private_key_id'] = os.getenv("G_API_KEY_ID")
    data['private_key'] = os.getenv("G_API_KEY").replace('\\n', '\n')
    data['client_email'] = os.getenv("G_API_MAIL")
    data['client_id'] = os.getenv("G_API_C_ID")
    data['client_x509_cert_url'] = os.getenv("G_API_CURL")
    set_data(data,g_file)

    g_file_location = dir_path + '/cogs/' + g_file + '.json'
    gc = gspread.service_account(filename = g_file_location)
    sh = gc.open('DiscordUserdata')
    return sh.worksheet("Data")

googleData = CreateGspread()
intentGuilds = int( googleData.acell(f'A20').value )

intents = interactions.Intents.GUILD_MEMBERS | interactions.Intents.GUILD_MESSAGES | interactions.Intents.GUILD_MESSAGE_REACTIONS | interactions.Intents.DIRECT_MESSAGES | interactions.Intents.GUILDS

bot = interactions.Client(
    token=os.getenv("DISCORD_TOKEN"),
    intents=intents,
    presence=interactions.ClientPresence(
        status=interactions.StatusType.ONLINE,
        activities=[interactions.PresenceActivity(
            type=interactions.PresenceActivityType.WATCHING,
            name=f"in {intentGuilds} servers."
        )]
    ), 
    disable_sync=False)

global list_guild_ids
list_guild_ids = []

async def getNumberGuilds():
    guild_list = await bot._http.get_self_guilds()
    for guild in guild_list:
        list_guild_ids.append( int( guild["id"] ) )

@bot.event 
async def on_ready():
    print(f"Logged in as {bot.me.name}({bot.me.id})")
    channel = interactions.Channel(**await bot._http.get_channel( int( os.getenv("LOGS")) ), _client=bot._http)

    await getNumberGuilds()
    numberGuild = len(list_guild_ids)
    googleData.update_acell(f'A20',str(numberGuild))

    time = datetime.datetime.utcnow()
    await channel.send(f"[{time}] [STARTUP] Logged in in {numberGuild} servers!{os.linesep}{list_guild_ids}")
    #await bot._websocket._update_presence(interactions.ClientPresence(status=interactions.StatusType.ONLINE,activities=[interactions.PresenceActivity(name=f'in {len(list_guild_ids)} servers',type=interactions.PresenceActivityType.GAME)]))

# load cogs
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        print(f'[COGS] Unable to load {filename}')

# Create bot
bot.start()
