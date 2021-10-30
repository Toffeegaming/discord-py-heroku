import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

import json
import random as rand

from discord_slash.utils.manage_commands import generate_options

#guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3"))]
guild_ids = [int(os.getenv("GUILD3"))]

class Roulette(Cog):
    def __init__(self, bot: Bot):
        self.bot = bot

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
        "Ace in the Hole",######### https://deadbydaylight.fandom.com/wiki/Perks
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole",
        "Ace in the Hole"
    ]

    def SelectPerks(self, in_seed, in_range):
        rand.seed(in_seed)
        generatedList = rand.sample(range(in_range),4)
        return generatedList

    def get_data(self):
        with open("roulette_userdata.json", 'r') as file:
            return json.loads(file.read())

    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 97)
    
        await ctx.send(f"{ctx.author} krijgt: {self.SurvivorPerks[generatedPerks[0]]} {self.SurvivorPerks[generatedPerks[1]]} {self.SurvivorPerks[generatedPerks[2]]} {self.SurvivorPerks[generatedPerks[3]]}")

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        await ctx.send(f"Under construction :)")

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
