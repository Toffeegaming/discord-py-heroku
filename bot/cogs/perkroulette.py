import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

import json
import requests
import random as rand
from contextlib import suppress

from discord_slash.utils.manage_commands import generate_options

guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3"))]

class Roulette(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

    SurvivorPerks = [ ######### https://deadbydaylight.fandom.com/wiki/Perks
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

    def get_request():
        with suppress(NameError):
            request = {
                "jsonrpc": "2.0",
                "method": "generateIntegerSequences",
                "params": {
                    "apiKey": os.getenv("RANDOM-API"),
                    "n": 1,
                    "length": 4,
                    "min": 0,
                    "max": in_range,
                    "replacement": false,
                    "base": 10
                },
                "id": in_id
            }
            response = requests.post('https://api.random.org/json-rpc/4/invoke',
            data=json.dumps(request),
            headers={'content-type': 'application/json'})
            
            data = response.json()
            return data


    def SelectPerks(self, in_id, in_range):
        roaData = get_request()

        print(roaData)
        # result = response["result"]
        # data = result["random"]
        # print(data)
        generatedList = rand.sample(range(in_range),4)
        return generatedList

    def get_data(self):
        with open("roulette_userdata.json", 'r') as file:
            return json.loads(file.read())

    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 97)
        await ctx.send(f"{ctx.author.name} krijgt:{os.linesep}{self.SurvivorPerks[generatedPerks[0]]}{os.linesep}{self.SurvivorPerks[generatedPerks[1]]}{os.linesep}{self.SurvivorPerks[generatedPerks[2]]}{os.linesep}{self.SurvivorPerks[generatedPerks[3]]}")

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        await ctx.send(f"Under construction :)")

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
