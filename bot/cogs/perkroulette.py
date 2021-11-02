import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

import discord
import json
import gspread
import requests

from discord_slash.utils.manage_commands import generate_options

guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3"))]



class Roulette(Cog):
    def __init__(self, bot: Bot, google_Data):
        self.bot = bot
        
        g_file = 'jsonfiles/google_api_secret'
        data = self.get_data(g_file)
        data['project_id'] = os.getenv("G_API_ID")
        data['private_key_id'] = os.getenv("G_API_KEY_ID")
        data['private_key'] = os.getenv("G_API_KEY")
        data['client_email'] = os.getenv("G_API_MAIL")
        data['client_id'] = os.getenv("G_API_C_ID")
        data['client_x509_cert_url'] = os.getenv("G_API_CURL")
        self.set_data(data,g_file)

        g_dir_path = os.path.dirname(os.path.realpath(__file__))
        g_file_location = g_dir_path + '/' + g_file + '.json'
        gc = gspread.service_account(filename = g_file_location)
        sh = gc.open('DiscordUserdata')
        self.google_Data = sh.worksheet("Data")

    #----------------------------------------------------------------------------------
    # Variables
    # https://deadbydaylight.fandom.com/wiki/Perks

    SurvivorPerks = [
        "Ace in the Hole",
        "Adrenaline",
        "Aftercare",
        "Alert",
        "Any Means Necessary",
        "Appraisal",
        "Autodidact",
        "Balanced Landing",
        "Bite the Bullet",
        "Blast Mine",
        "Blood Pact",
        "Boil Over",
        "Bond",
        "Boon: Circle of Healing",
        "Boon: Shadow Step",
        "Borrowed Time",
        "Botany Knowledge",
        "Breakdown",
        "Breakout",
        "Buckle Up",
        "Built to Last",
        "Calm Spirit",
        "Clairvoyance",
        "Counterforce",
        "Dance With Me",
        "Dark Sense",
        "Dead Hard",
        "Deception",
        "Decisive Strike",
        "Deliverance",
        "Desperate Measures",
        "Detective's Hunch",
        "Distortion",
        "Diversion",
        "Déjà Vu",
        "Empathy",
        "Fast Track",
        "Flashbang",
        "Flip-Flop",
        "For the People",
        "Guardian",
        "Head On",
        "Hope",
        "Inner Healing",
        "Iron Will",
        "Kindred",
        "Kinship",
        "Leader",
        "Left Behind",
        "Lightweight",
        "Lithe",
        "Lucky Break",
        "Mettle of Man",
        "No Mither",
        "No One Left Behind",
        "Object of Obsession",
        "Off the Record",
        "Open-Handed",
        "Pharmacy",
        "Plunderer's Instinct",
        "Poised",
        "Power Struggle",
        "Premonition",
        "Prove Thyself",
        "Quick & Quiet",
        "Red Herring",
        "Renewal",
        "Repressed Alliance",
        "Resilience",
        "Resurgence",
        "Rookie Spirit",
        "Saboteur",
        "Self-Aware",
        "Self-Care",
        "Self-Preservation",
        "Situational Awareness",
        "Slippery Meat",
        "Small Game",
        "Smash Hit",
        "Sole Survivor",
        "Solidarity",
        "Soul Guard",
        "Spine Chill",
        "Sprint Burst",
        "Stake Out",
        "Streetwise",
        "Technician",
        "Tenacity",
        "This Is Not Happening",
        "Unbreakable",
        "Up the Ante",
        "Urban Evasion",
        "Vigil",
        "Visionary",
        "Wake Up!",
        "We'll Make It",
        "We're Gonna Live Forever",
        "Windows of Opportunity"
    ]

    KillerPerks = [
        "A Nurse's Calling",
        "Agitation",
        "Bamboozle",
        "Barbecue & Chilli",
        "Beast of Prey",
        "Bitter Murmur",
        "Blood Echo",
        "Blood Warden",
        "Bloodhound",
        "Brutal Strength",
        "Claustrophobia",
        "Corrupt Intervention",
        "Coulrophobia",
        "Coup de Grâce",
        "Dark Devotion",
        "Dead Man's Switch",
        "Deadlock",
        "Deathbound",
        "Deerstalker",
        "Discordance",
        "Distressing",
        "Dragon's Grip",
        "Dying Light",
        "Enduring",
        "Eruption",
        "Fearmonger",
        "Fire Up",
        "Forced Penance",
        "Franklin's Demise",
        "Furtive Chase",
        "Gearhead",
        "Hangman's Trick",
        "Hex: Blood Favour",
        "Hex: Crowd Control",
        "Hex: Devour Hope",
        "Hex: Haunted Ground",
        "Hex: Huntress Lullaby",
        "Hex: No One Escapes Death",
        "Hex: Plaything",
        "Hex: Retribution",
        "Hex: Ruin",
        "Hex: The Third Seal",
        "Hex: Thrill of the Hunt",
        "Hex: Undying",
        "Hoarder",
        "Hysteria",
        "I'm All Ears",
        "Infectious Fright",
        "Insidious",
        "Iron Grasp",
        "Iron Maiden",
        "Jolt",
        "Knock Out",
        "Lethal Pursuer",
        "Lightborn",
        "Mad Grit",
        "Make Your Choice",
        "Monitor & Abuse",
        "Monstrous Shrine",
        "Nemesis",
        "No Way Out",
        "Oppression",
        "Overcharge",
        "Overwhelming Presence",
        "Play with Your Food",
        "Pop Goes the Weasel",
        "Predator",
        "Rancor",
        "Remember Me",
        "Save the Best for Last",
        "Scourge Hook: Gift of Pain",
        "Shadowborn",
        "Sloppy Butcher",
        "Spies from the Shadows",
        "Spirit Fury",
        "Starstruck",
        "Stridor",
        "Surveillance",
        "Territorial Imperative",
        "Thanatophobia",
        "Thrilling Tremors",
        "Tinkerer",
        "Trail of Torment",
        "Unnerving Presence",
        "Unrelenting",
        "Whispers",
        "Zanshin Tactics"
    ]

    #----------------------------------------------------------------------------------
    # Methods
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

    def get_Google_data(self):
        return True

    def set_Google_data(self):
        return True

    def createProfile(self,discord_id):
        data = self.get_data()
        data.append({"discord_id":discord_id,"data":{"survP":[-1],"killP":[-1]}})
        self.set_data(data)
        print(f'Created {discord_id} profile')

    def resetProfile(self,discord_id, mode):
        data = self.get_data()
        team = ''
        if mode == 'survivor':
            team = 'survP'

        if mode == 'killer':
            team = 'killP'

        if mode == 'both':
            for profile in data:
                if profile['discord_id'] == discord_id:
                    profile['data']['survP'] = [-1]
                    profile['data']['killP'] = [-1]
            self.set_data(data)
            print(f'Reset {discord_id} full profile')
            return True

        for profile in data:
            if profile['discord_id'] == discord_id:
                profile['data'][team] = [-1]
        self.set_data(data)
        print(f'Reset {discord_id} {team} profile')
        return True

    def add_allPerks(self,discord_id,mode):
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
                length = 0
                if mode == 'survivor':
                    length = len(self.SurvivorPerks)
                elif mode == 'killer':
                    length = len(self.KillerPerks)

                perklist = [0] * length

                for x in range(length):
                    perklist[x] = x
                profile['data'][perksToModify] = perklist
        self.set_data(data)
        print('Modified perks')
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

    def modify_Perks(self,discord_id,character,mode):
        data = self.get_data()
        perksToModify = [-1,-1,-1]
        team = ''

        while True:
            if character == 'defaultS':
                perksToModify = [25,34,42,45,49,54,59,62,68,76,77,82,88,95,43,75,72,66,46,40]
                team = 'survP'
                break
            elif character == 'Meg':
                perksToModify = [64,83,1]
                team = 'survP'
                break
            elif character == 'Dwight':
                perksToModify = [12,63,47]
                team = 'survP'
                break
            elif character == 'Claudette':
                perksToModify = [35,16,73]
                team = 'survP'
                break
            elif character == 'Jake':
                perksToModify = [44,21,71]
                team = 'survP'
                break
            elif character == 'Nea':
                perksToModify = [7,91,85]
                team = 'survP'
                break
            elif character == 'Laurie':
                perksToModify = [79,55,28]
                team = 'survP'
                break
            elif character == 'Ace':
                perksToModify = [90,57,0]
                team = 'survP'
                break
            elif character == 'Bill':
                perksToModify = [48,15,89]
                team = 'survP'
                break
            elif character == 'Min':
                perksToModify = [86,50,3]
                team = 'survP'
                break
            elif character == 'David':
                perksToModify = [96,26,53]
                team = 'survP'
                break
            elif character == 'Quentin':
                perksToModify = [94,58,92]
                team = 'survP'
                break
            elif character == 'Tapp':
                perksToModify = [87,31,84]
                team = 'survP'
                break
            elif character == 'Kate':
                perksToModify = [24,97,11]
                team = 'survP'
                break
            elif character == 'Adam':
                perksToModify = [33,29,6]
                team = 'survP'
                break
            elif character == 'Jeff':
                perksToModify = [17,2,32]
                team = 'survP'
                break
            elif character == 'Jane':
                perksToModify = [80,60,41]
                team = 'survP'
                break
            elif character == 'Ash':
                perksToModify = [38,19,52]
                team = 'survP'
                break
            elif character == 'Nancy':
                perksToModify = [43,75,72]
                team = 'survP'
                break
            elif character == 'Steve':
                perksToModify = [66,46,40]
                team = 'survP'
                break
            elif character == 'Yui':
                perksToModify = [51,4,18]
                team = 'survP'
                break
            elif character == 'Zarina':
                perksToModify = [65,58,39]
                team = 'survP'
                break
            elif character == 'Cheryl':
                perksToModify = [81,10,67]
                team = 'survP'
                break
            elif character == 'Felix':
                perksToModify = [93,30,20]
                team = 'survP'
                break
            elif character == 'Elodie':
                perksToModify = [5,27,61]
                team = 'survP'
                break
            elif character == 'Yunjin':
                perksToModify = [36,78,74]
                team = 'survP'
                break
            elif character == 'Jill':
                perksToModify = [23,69,9]
                team = 'survP'
                break
            elif character == 'Leon':
                perksToModify = [8,37,70]
                team = 'survP'
                break
            elif character == 'Mikaela':
                perksToModify = [22,13,14]
                team = 'survP'
                break
            else:
                return False

        for profile in data:
                if profile['discord_id'] == discord_id:
                    perklist = profile['data'][team]

                    if -1 in perklist:
                        perklist.remove(-1)

                    if mode == 'add':
                        for item in perksToModify:
                            if item not in perklist:
                                perklist.append(perksToModify[item])
                    elif mode == 'delete':
                        for item in perksToModify:
                            if item in perklist:
                                perklist.remove(item)

        self.set_data(data)
        print(f'Modified {discord_id} {team} perks')
        return True

    def check_profile(self,discord_id):
        return self.google_Data.find(str(discord_id))


    #----------------------------------------------------------------------------------
    # Commands

    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        id = ctx.author_id

        print(self.check_profile(id))

        generatedPerks = self.SelectPerks(id, 97)
        embed = discord.Embed(
            title="Survivor Roulette!",
            description=f"{ctx.author.name} krijgt:{os.linesep}{self.SurvivorPerks[generatedPerks[0]]}{os.linesep}{self.SurvivorPerks[generatedPerks[1]]}{os.linesep}{self.SurvivorPerks[generatedPerks[2]]}{os.linesep}{self.SurvivorPerks[generatedPerks[3]]}",
            color=int("0x9628f7",16))
        embed.set_footer(text="Gebruik de command opnieuw voor andere perks!")
        await ctx.send(embed=embed)
        
        # jData = self.get_data()
        # id = ctx.author_id

        # if not self.check_profile(jData,id):
        #     self.createProfile(id)
        #     self.add_allPerks(id,'survivor')

        # for profile in jData:
        #     if profile['discord_id'] == id:
        #         availablePerks = profile['data']['survP']
        #         numberPerks = len(availablePerks)
        #         print(numberPerks)
        #         if not numberPerks >= 4:
        #             embed = discord.Embed(
        #             title=":(",
        #             description=f"Het lijkt erop dat je niet genoeg perks hebt aan staan om een build te kunnen maken!",
        #             color=int("0x9628f7",16))
        #             await ctx.send(embed=embed)

        #         generatedPerks = self.SelectPerks(id, len(availablePerks))

        #         namedPerks = [
        #             self.SurvivorPerks[availablePerks[generatedPerks[0]]],
        #             self.SurvivorPerks[availablePerks[generatedPerks[1]]],
        #             self.SurvivorPerks[availablePerks[generatedPerks[2]]],
        #             self.SurvivorPerks[availablePerks[generatedPerks[3]]]
        #             ]

        #         embed = discord.Embed(
        #             title="Survivor Roulette!",
        #             description=f"{ctx.author.name} krijgt:{os.linesep}{namedPerks[0]}{os.linesep}{namedPerks[1]}{os.linesep}{namedPerks[2]}{os.linesep}{namedPerks[3]}",
        #             color=int("0x9628f7",16))
        #         embed.set_footer(text="Gebruik de command opnieuw voor andere perks!")
        #         await ctx.send(embed=embed)
        #         return True

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 86)
        embed = discord.Embed(
            title="Killer Roulette!",
            description=f"{ctx.author.name} krijgt:{os.linesep}{self.KillerPerks[generatedPerks[0]]}{os.linesep}{self.KillerPerks[generatedPerks[1]]}{os.linesep}{self.KillerPerks[generatedPerks[2]]}{os.linesep}{self.KillerPerks[generatedPerks[3]]}",
            color=int("0x9628f7",16))
        embed.set_footer(text="Gebruik de command opnieuw voor andere perks!")
        await ctx.send(embed=embed)

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
