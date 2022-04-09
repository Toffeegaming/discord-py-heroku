import interactions, os, sys, datetime, gspread

dir_path = os.path.dirname(os.path.realpath(__file__))
sys.path.append(dir_path)

def CreateGspread():
    credentials = {
    "type": "service_account",
    "project_id": str(os.getenv("G_API_ID") ),
    "private_key_id": str(os.getenv("G_API_KEY_ID") ),
    "private_key": str(os.getenv("G_API_KEY").replace('\\n', '\n') ),
    "client_email": str(os.getenv("G_API_MAIL") ),
    "client_id": str(os.getenv("G_API_C_ID") ),
    "auth_uri": "https://accounts.google.com/o/oauth2/auth",
    "token_uri": "https://oauth2.googleapis.com/token",
    "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
    "client_x509_cert_url": str(os.getenv("G_API_CURL") )
    }

    gc = gspread.service_account_from_dict(credentials)
    sh = gc.open('DiscordUserdata')
    return sh

googleData = CreateGspread()
sheet = googleData.worksheet("ServerList")

intentGuilds = sheet.acell(f'{ str(os.getenv("DISCORD_SERVERCOUNT") ) }').value

intents = interactions.Intents.GUILD_MEMBERS | interactions.Intents.GUILD_MESSAGES | interactions.Intents.GUILD_MESSAGE_REACTIONS | interactions.Intents.DIRECT_MESSAGES | interactions.Intents.GUILDS

bot = interactions.Client(
    token=os.getenv("DISCORD_TOKEN"),
    intents=intents,
    presence=interactions.ClientPresence(
        status=interactions.StatusType.ONLINE,
        activities=[interactions.PresenceActivity(
            type=interactions.PresenceActivityType.WATCHING,
            name=f"in {intentGuilds} servers"
        )]
    ), 
    disable_sync=False)

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
    sheet.update_acell(f'{ str(os.getenv("DISCORD_SERVERCOUNT") ) }',str(numberGuild))

    time = datetime.datetime.utcnow()
    await channel.send(f"[{time}] [STARTUP] Logged in in {numberGuild} servers!{os.linesep}{list_guild_ids}")

@bot.event
async def on_guild_member_add(ctx):
    guild_id = int( ctx.guild_id )
    print(guild_id)
    if not guild_id == 956152709034164224:
        print("GuidId incorrect")
        return
    print("GuidId correct")

    googleData = CreateGspread()
    sheet = googleData.worksheet("RoleData")

    row = sheet.find(str(ctx.user.id))

    if row is not None:
        print("userdata exists")
        return
    print("userdata does not exist")

    counter = int( sheet.acell(f'C1').value ) + 1

    sheet.update_acell(f'A{counter}',str(ctx.user.id))

    roleData = {
        "name" : str(ctx.user.username),
        "color" : int('0xffffff',16),
        "position" : 2,
        'permissions': '0'
    
    }

    newrole = await bot._http.create_guild_role(guild_id=guild_id,data=roleData)
    print("made new role")
    newrole_id = newrole["id"]

    await bot._http.add_member_role(guild_id=guild_id, user_id=ctx.user.id, role_id=newrole_id)
    print("added new role to user")  

    sheet.update_acell(f'B{counter}',str(newrole_id))
    print("updated data")


# load cogs
for filename in os.listdir(dir_path + '/cogs'):
    if filename.endswith('.py'):
        bot.load(f'cogs.{filename[:-3]}')
        print(f"[COGS] loaded {filename[:-3]}")
    else:
        print(f'[COGS] Unable to load {filename}')


import aiocron
from flask import Flask
from threading import Thread
#from werkzeug.serving import make_server

# class ServerThread(Thread):

#     def __init__(self, app):
#         Thread.__init__(self)
#         self.server = make_server('0.0.0.0', 5000, app)
#         self.ctx = app.app_context()
#         self.ctx.push()

#     def run(self):
#         print(f'starting server')
#         self.server.serve_forever()

#     def shutdown(self):
#         self.server.shutdown()

# def stop_server():
#     global server
#     server.shutdown()


app = Flask(__name__)
@app.route('/')
def index():
    return 'Bot is ready'

def run():
  app.run(host="0.0.0.0", port=8000)

server = Thread(target=run)
server.start()

# global server
# server = ServerThread(app)
# server.start()
print(f'server started')

# cronjob
@aiocron.crontab('* * * * *')
async def message():
    try:
        print(bot.latency)
    except:
        server.join()


# Create bot
bot.start()