import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext, ComponentContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component
from discord_slash.utils.manage_commands import create_option, create_choice
from discord_slash.model import ButtonStyle

import discord
import json
import gspread
import requests

guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3"))]

class Roulette(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot
        self.googleData = None
        self.Color = int("0x9628f7",16)
        self.LogChannel = int(os.getenv("LOGS"))
    #----------------------------------------------------------------------------------
    # Variables
    # https://deadbydaylight.fandom.com/wiki/Perks
    SurvivorPerks = ["Ace in the Hole","Adrenaline","Aftercare","Alert","Any Means Necessary","Appraisal","Autodidact","Balanced Landing","Bite the Bullet","Blast Mine","Blood Pact","Boil Over","Bond","Boon: Circle of Healing","Boon: Shadow Step","Borrowed Time","Botany Knowledge","Breakdown","Breakout","Buckle Up","Built to Last","Calm Spirit","Clairvoyance","Counterforce","Dance With Me","Dark Sense","Dead Hard","Deception","Decisive Strike","Deliverance","Desperate Measures","Detective's Hunch","Distortion","Diversion","Déjà Vu","Empathy","Fast Track","Flashbang","Flip-Flop","For the People","Guardian","Head On","Hope","Inner Healing","Iron Will","Kindred","Kinship","Leader","Left Behind","Lightweight","Lithe","Lucky Break","Mettle of Man","No Mither","No One Left Behind","Object of Obsession","Off the Record","Open-Handed","Pharmacy","Plunderer's Instinct","Poised","Power Struggle","Premonition","Prove Thyself","Quick & Quiet","Red Herring","Renewal","Repressed Alliance","Resilience","Resurgence","Rookie Spirit","Saboteur","Self-Aware","Self-Care","Self-Preservation","Situational Awareness","Slippery Meat","Small Game","Smash Hit","Sole Survivor","Solidarity","Soul Guard","Spine Chill","Sprint Burst","Stake Out","Streetwise","Technician","Tenacity","This Is Not Happening","Unbreakable","Up the Ante","Urban Evasion","Vigil","Visionary","Wake Up!","We'll Make It","We're Gonna Live Forever","Windows of Opportunity"]

    KillerPerks = ["A Nurse's Calling","Agitation","Bamboozle","Barbecue & Chilli","Beast of Prey","Bitter Murmur","Blood Echo","Blood Warden","Bloodhound","Brutal Strength","Claustrophobia","Corrupt Intervention","Coulrophobia","Coup de Grâce","Dark Devotion","Dead Man's Switch","Deadlock","Deathbound","Deerstalker","Discordance","Distressing","Dragon's Grip","Dying Light","Enduring","Eruption","Fearmonger","Fire Up","Forced Penance","Franklin's Demise","Furtive Chase","Gearhead","Hangman's Trick","Hex: Blood Favour","Hex: Crowd Control","Hex: Devour Hope","Hex: Haunted Ground","Hex: Huntress Lullaby","Hex: No One Escapes Death","Hex: Plaything","Hex: Retribution","Hex: Ruin","Hex: The Third Seal","Hex: Thrill of the Hunt","Hex: Undying","Hoarder","Hysteria","I'm All Ears","Infectious Fright","Insidious","Iron Grasp","Iron Maiden","Jolt","Knock Out","Lethal Pursuer","Lightborn","Mad Grit","Make Your Choice","Monitor & Abuse","Monstrous Shrine","Nemesis","No Way Out","Oppression","Overcharge","Overwhelming Presence","Play with Your Food","Pop Goes the Weasel","Predator","Rancor","Remember Me","Save the Best for Last","Scourge Hook: Gift of Pain","Shadowborn","Sloppy Butcher","Spies from the Shadows","Spirit Fury","Starstruck","Stridor","Surveillance","Territorial Imperative","Thanatophobia","Thrilling Tremors","Tinkerer","Trail of Torment","Unnerving Presence","Unrelenting","Whispers","Zanshin Tactics"]

    #----------------------------------------------------------------------------------
    # Methods
    def get_data(self,name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_location = dir_path + '/' + name + '.json'
        with open(file_location, 'r') as file:
            return json.loads(file.read())
    
    def set_data(self,data,name):
        dir_path = os.path.dirname(os.path.realpath(__file__))
        file_location = dir_path + '/' + name + '.json'
        with open(file_location, 'w') as file:
            file.write(json.dumps(data, indent=2))

    def check_connection(self):
        if self.googleData is None:
            self._CreateGspread()
        return True

    def check_profile(self,discord_id):
        return self.googleData.find(str(discord_id))

    def _CreateGspread(self):
        g_file = 'jsonfiles/google_api_secret'
        data = self.get_data(g_file)
        data['project_id'] = os.getenv("G_API_ID")
        data['private_key_id'] = os.getenv("G_API_KEY_ID")
        data['private_key'] = os.getenv("G_API_KEY").replace('\\n', '\n')
        data['client_email'] = os.getenv("G_API_MAIL")
        data['client_id'] = os.getenv("G_API_C_ID")
        data['client_x509_cert_url'] = os.getenv("G_API_CURL")
        self.set_data(data,g_file)

        dir_path = os.path.dirname(os.path.realpath(__file__))
        g_file_location = dir_path + '/' + g_file + '.json'
        gc = gspread.service_account(filename = g_file_location)
        sh = gc.open('DiscordUserdata')
        self.googleData = sh.worksheet("Data")
        return True

    def get_Google_dataRow(self, discord_id):
        return self.googleData.find(str(discord_id)).row

    def set_Google_data(self, row, perksToModify, value):
        column = ""

        if perksToModify == 'survivor':
            column = "B"
        elif perksToModify == 'killer':
            column = "C"
        else:
            return False

        self.googleData.update_acell(f'{column}{row}',str(value))
        return True

    def g_next_available_row(self):
        str_list = list(filter(None, self.googleData.col_values(1)))
        return str(len(str_list)+1)

    async def createProfile(self,discord_id):
        available = self.g_next_available_row()
        self.googleData.update_acell(f"A{available}", str(discord_id))
        arr = [-1]
        self.set_Google_data(available,'survivor',arr)
        self.set_Google_data(available,'killer',arr)
        print(f'[PROFILE] Created {discord_id} profile')
        await self.bot.get_channel( self.LogChannel ).send(f'[PROFILE] Created {discord_id} profile')

    def resetProfile(self,discord_id, mode):
        row = self.get_Google_dataRow(discord_id)
        arr = [-1]

        if mode == 'both':
            self.set_Google_data(row,'survP',arr)
            self.set_Google_data(row,'killP',arr)
            return True
        else:
            self.set_Google_data(row,mode.arr)

        return False

    def add_allPerks(self,discord_id,mode):
        row = self.get_Google_dataRow(discord_id)

        length = 0

        if mode == 'survivor':
            length = len(self.SurvivorPerks)
        elif mode == 'killer':
            length = len(self.KillerPerks)
        else:
            return False

        perklist = [0] * length

        for x in range(length):
            perklist[x] = x

        self.set_Google_data(row,mode, perklist)
        return True

    def delete_allPerks(self,discord_id,mode):
        data = self.get_data()
        perksToModify = ""
        if mode == 'survivor':
            perksToModify = "survP"
        elif mode == 'killer':
            perksToModify = "killP"
        else:
            return False

        for profile in data:
                if profile['discord_id'] == discord_id:
                    perklist = [0]
                    profile['data'][perksToModify] = perklist
        self.set_data(data)
        print('Modified perks')
        return True

    async def modify_Perks(self,ctx: SlashContext,character,mode):
        waitingEmbed = discord.Embed(
                title=f"",
                description=f"Je perks worden aangepast...",
                color=self.Color)
        msg = await ctx.send(embed=waitingEmbed)

        discord_id = id = ctx.author_id
        row = self.get_Google_dataRow(discord_id)

        perksToModify = [-1,-1,-1]
        team = ''

        while True:
            if character == 'defaultS':
                perksToModify = [25,34,42,45,49,54,59,62,68,76,77,82,88,95,43,75,72,66,46,40]
                team = 'B'
                break
            elif character == 'Meg':
                perksToModify = [64,83,1]
                team = 'B'
                break
            elif character == 'Dwight':
                perksToModify = [12,63,47]
                team = 'B'
                break
            elif character == 'Claudette':
                perksToModify = [35,16,73]
                team = 'B'
                break
            elif character == 'Jake':
                perksToModify = [44,21,71]
                team = 'B'
                break
            elif character == 'Nea':
                perksToModify = [7,91,85]
                team = 'B'
                break
            elif character == 'Laurie':
                perksToModify = [79,55,28]
                team = 'B'
                break
            elif character == 'Ace':
                perksToModify = [90,57,0]
                team = 'B'
                break
            elif character == 'Bill':
                perksToModify = [48,15,89]
                team = 'B'
                break
            elif character == 'Min':
                perksToModify = [86,50,3]
                team = 'B'
                break
            elif character == 'David':
                perksToModify = [96,26,53]
                team = 'B'
                break
            elif character == 'Quentin':
                perksToModify = [94,58,92]
                team = 'B'
                break
            elif character == 'Tapp':
                perksToModify = [87,31,84]
                team = 'B'
                break
            elif character == 'Kate':
                perksToModify = [24,97,11]
                team = 'B'
                break
            elif character == 'Adam':
                perksToModify = [33,29,6]
                team = 'B'
                break
            elif character == 'Jeff':
                perksToModify = [17,2,32]
                team = 'B'
                break
            elif character == 'Jane':
                perksToModify = [80,60,41]
                team = 'B'
                break
            elif character == 'Ash':
                perksToModify = [38,19,52]
                team = 'B'
                break
            elif character == 'Nancy':
                perksToModify = [43,75,72]
                team = 'B'
                break
            elif character == 'Steve':
                perksToModify = [66,46,40]
                team = 'B'
                break
            elif character == 'Yui':
                perksToModify = [51,4,18]
                team = 'B'
                break
            elif character == 'Zarina':
                perksToModify = [65,58,39]
                team = 'B'
                break
            elif character == 'Cheryl':
                perksToModify = [81,10,67]
                team = 'B'
                break
            elif character == 'Felix':
                perksToModify = [93,30,20]
                team = 'B'
                break
            elif character == 'Elodie':
                perksToModify = [5,27,61]
                team = 'B'
                break
            elif character == 'Yunjin':
                perksToModify = [36,78,74]
                team = 'B'
                break
            elif character == 'Jill':
                perksToModify = [23,69,9]
                team = 'B'
                break
            elif character == 'Leon':
                perksToModify = [8,37,70]
                team = 'B'
                break
            elif character == 'Mikaela':
                perksToModify = [22,13,14]
                team = 'B'
                break
            else:
                return False

        g_value = self.googleData.acell(f"{team}{row}").value
        
        stripVal = g_value.lstrip("[").rstrip("]")
        availablePerks = list(map(int,stripVal.split(", ")))


        if -1 in availablePerks:
            availablePerks.remove(-1)

        if mode=="add":
            for x in range(len(perksToModify)):
                if perksToModify[x] not in availablePerks:
                    availablePerks.append(perksToModify[x])
            if team == "B":
                self.set_Google_data(row, 'survivor', availablePerks)
            else:
                self.set_Google_data(row, 'killer', availablePerks)
        elif mode=="delete":
            for x in range(len(perksToModify)):
                if perksToModify[x] in availablePerks:
                    availablePerks.remove(perksToModify[x])
            if team == "B":
                self.set_Google_data(row, 'survivor', availablePerks)
            else:
                self.set_Google_data(row, 'killer', availablePerks)

        print(f'Modified {discord_id} perks')
        modifyEmbed = discord.Embed(
                title=f"",
                description=f"Je perks zijn aangepast",
                color=self.Color)
        await msg.edit(embed=modifyEmbed)
        return True

    def SelectPerks(self, in_id, in_range):
        bool = False
        request = {
            "jsonrpc": "2.0",
            "method": "generateIntegerSequences",
            "params": {
                "apiKey": os.getenv("RANDOM-API"),
                "n": 1,
                "length": 4,
                "min": 0,
                "max": in_range,
                "replacement": bool,
                "base": 10
            },
            "id": in_id
        }

        response = requests.post('https://api.random.org/json-rpc/4/invoke',
        data=json.dumps(request),
        headers={'content-type': 'application/json'})
        data = response.json()
        generatedList = data['result']['random']['data'][0]
        return generatedList

    async def PerkMaker(self,ctx: SlashContext, mode,prev_msg=None):
        id = ctx.author_id
        
        if prev_msg is None:
            waitingEmbed = discord.Embed(
                title=f"{mode} Roulette!",
                description=f"Je perks worden uitgekozen...",
                color=self.Color)
            msg = await ctx.send(embed=waitingEmbed)
        else:
            msg = prev_msg

        if self.check_profile(id) is None:
            profileEmbed = discord.Embed(
            title=f"{mode} Roulette!",
            description=f"Profiel wordt aangemaakt, je krijgt zo je perks...",
            color=self.Color)
            await msg.edit(embed=profileEmbed)
            await self.createProfile(id)
            
            self.add_allPerks(id,'survivor') #TODO remove?
            self.add_allPerks(id,'killer') #TODO remove?

        value = None
        if mode == 'Survivor':
            value = self.googleData.acell(f'B{self.get_Google_dataRow(id)}').value
        elif mode == 'Killer':
            value = self.googleData.acell(f'C{self.get_Google_dataRow(id)}').value
        
        stripVal = value.lstrip("[").rstrip("]")
        availablePerks = list(map(int,stripVal.split(", ")))
        numberPerks = len(availablePerks)

        if not numberPerks >= 4:
            embed = discord.Embed(
            title=":(",
            description=f"Het lijkt erop dat je niet genoeg perks hebt aan staan om een build te kunnen maken!",
            color=self.Color)
            await ctx.send(embed=embed)
        else:
            generatedPerks = self.SelectPerks(id,numberPerks-1)

            if mode == 'Survivor':
                namedPerks = [
                    self.SurvivorPerks[availablePerks[generatedPerks[0]]],
                    self.SurvivorPerks[availablePerks[generatedPerks[1]]],
                    self.SurvivorPerks[availablePerks[generatedPerks[2]]],
                    self.SurvivorPerks[availablePerks[generatedPerks[3]]]
                    ]
                buttons = [
                    create_button(
                        style=ButtonStyle.grey,
                        label="Reroll perks",
                        emoji="🔁"
                    )]
            elif mode == 'Killer':
                namedPerks = [
                    self.KillerPerks[availablePerks[generatedPerks[0]]],
                    self.KillerPerks[availablePerks[generatedPerks[1]]],
                    self.KillerPerks[availablePerks[generatedPerks[2]]],
                    self.KillerPerks[availablePerks[generatedPerks[3]]]
                    ]
                buttons = [
                    create_button(
                        style=ButtonStyle.grey,
                        label="Reroll perks",
                        emoji="🔁"
                    )]
            
            action_row = create_actionrow(*buttons)

            perkEmbed = discord.Embed(
                title=f"{mode} Roulette!",
                description=f"<@{ctx.author_id}> krijgt:{os.linesep}{namedPerks[0]}{os.linesep}{namedPerks[1]}{os.linesep}{namedPerks[2]}{os.linesep}{namedPerks[3]}",
                color=self.Color)
            perkEmbed.set_footer(text=f"Gebruik de command opnieuw voor andere perks{os.linesep}of druk binnen 1 minuut op de reroll knop!")
            await msg.edit(embed=perkEmbed, components=[action_row])
            
            userHasReplied = False
            while not userHasReplied:
                try:
                    button_ctx: ComponentContext = await wait_for_component(self.bot,msg,components=action_row,timeout=60)
                    b_id = button_ctx.author_id
                    if id == b_id:
                        userHasReplied = True
                        waitingEmbed = discord.Embed(
                            title=f"{mode} Roulette!",
                            description=f"Je perks worden uitgekozen...",
                            color=self.Color)
                        await button_ctx.edit_origin(embed=waitingEmbed,components=None)
                        await self.PerkMaker(button_ctx,mode,msg)
                except:
                    userHasReplied = True
                    expiredEmbed = discord.Embed(
                        title=f"{mode} Roulette!",
                        description=f"<@{ctx.author_id}> krijgt:{os.linesep}{namedPerks[0]}{os.linesep}{namedPerks[1]}{os.linesep}{namedPerks[2]}{os.linesep}{namedPerks[3]}",
                        color=self.Color)
                    expiredEmbed.set_footer(text=f"Gebruik de command opnieuw voor andere perks!")
                    await msg.edit(embed=expiredEmbed,components=[])

    #----------------------------------------------------------------------------------
    # Commands

    # Main commands
    @cog_ext.cog_slash(name="Survivor", description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        self.check_connection()
        await self.PerkMaker(ctx,'Survivor')

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        self.check_connection()
        await self.PerkMaker(ctx,'Killer')

    @cog_ext.cog_slash(
        name="AddSurvivor",
        description="Voeg de 3 perks van een survivor toe.",
        options=[
            create_option(
                name="Naam",
                description="Dit is de survivor van wie de perks worden toegevoegd aan je lijst.",
                option_type=3,
                required=True,
                choices=[create_choice(name="Default perks",value="defaultS"),create_choice(name="Ace",value="Ace"),create_choice(name="Adam",value="Adam"),create_choice(name="Ash",value="Ash"),create_choice(name="Bill",value="Bill"),create_choice(name="Cheryl",value="Cheryl"),create_choice(name="Claudette",value="Claudette"),create_choice(name="David",value="David"),create_choice(name="Dwight",value="Dwight"),create_choice(name="Felix",value="Felix"),create_choice(name="Jake",value="Jake"),create_choice(name="Jane",value="Jane"),create_choice(name="Jeff",value="Jeff"),create_choice(name="Jill",value="Jill"),create_choice(name="Kate",value="Kate"),create_choice(name="Laurie",value="Laurie"),create_choice(name="Leon",value="Leon"),create_choice(name="Meg",value="Mikaela"),create_choice(name="Min",value="Min"),create_choice(name="Nancy",value="Nancy"),create_choice(name="Nea",value="Nea"),create_choice(name="Quentin",value="Quentin"),create_choice(name="Steve",value="Steve"),create_choice(name="Tapp",value="Tapp"),create_choice(name="Yui",value="Yui"),create_choice(name="Yun-Jin",value="Yunjin"),create_choice(name="Zarina",value="Zarina"),create_choice(name="Élodie",value="Elodie")
                ]
            )
        ])
    async def AddSurvivor(self,ctx: SlashContext,Naam: str):
        await self.modify_Perks(ctx,Naam,'add')


def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
