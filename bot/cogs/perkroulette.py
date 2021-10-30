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

    SurvivorPerks = {
        {1: "Ace in the Hole"},
        {2: "Adrenaline"},
        {3: "Aftercare"},
        {4: "Alert"},
        {5: "Any Means Necessary"},
        {6: "Appraisal"},
        {7: "Autodidact"},
        {8: "Balanced Landing"},
        {9: "Bite the Bullet"},
        {10: "Blast Mine"},
        {11: "Blood Pact"},
        {12: "Boil Over"},
        {13: "Bond"},
        {14: "Boon: Circle of Healing"},
        {15: "Boon: Shadow Step"},
        {16: "Borrowed Time"},
        {17: "Botany Knowledge"},
        {18: "Breakdown"},
        {19: "Breakout"},
        {20: "Buckle Up"},
        {21: "Built to Last"},
        {22: "Calm Spirit"},
        {23: "Clairvoyance"},
        {24: "Counterforce"},
        {25: "Dance With Me"},
        {26: "Dark Sense"},
        {27: "Dead Hard"},
        {28: "Deception"},
        {29: "Decisive Strike"},
        {30: "Deliverance"},
        {31: "Desperate Measures"},
        {32: "Detective's Hunch"},
        {33: "Distortion"},
        {34: "Diversion"},
        {35: "Déjà Vu"},
        {36: "Empathy"},
        {37: "Fast Track"},
        {38: "Flashbang"},
        {39: "Flip-Flop"},
        {40: "For the People"},
        {41: "Guardian"},
        {42: "Head On"},
        {43: "Hope"},
        {44: "Inner Healing"},
        {45: "Iron Will"},
        {46: "Kindred"},
        {47: "Kinship"},
        {48: "Leader"},
        {49: "Left Behind"},
        {50: "Lightweight"},
        {51: "Lithe"},
        {52: "Lucky Break"},
        {53: "Ace in the Hole"},######### https://deadbydaylight.fandom.com/wiki/Perks
        {54: "Ace in the Hole"},
        {55: "Ace in the Hole"},
        {56: "Ace in the Hole"},
        {57: "Ace in the Hole"},
        {58: "Ace in the Hole"},
        {59: "Ace in the Hole"},
        {60: "Ace in the Hole"},
        {61: "Ace in the Hole"},
        {62: "Ace in the Hole"},
        {63: "Ace in the Hole"},
        {64: "Ace in the Hole"},
        {65: "Ace in the Hole"},
        {66: "Ace in the Hole"},
        {67: "Ace in the Hole"},
        {68: "Ace in the Hole"},
        {69: "Ace in the Hole"},
        {70: "Ace in the Hole"},
        {71: "Ace in the Hole"},
        {72: "Ace in the Hole"},
        {73: "Ace in the Hole"},
        {74: "Ace in the Hole"},
        {75: "Ace in the Hole"},
        {76: "Ace in the Hole"},
        {77: "Ace in the Hole"},
        {78: "Ace in the Hole"},
        {79: "Ace in the Hole"},
        {80: "Ace in the Hole"},
        {81: "Ace in the Hole"},
        {82: "Ace in the Hole"},
        {83: "Ace in the Hole"},
        {84: "Ace in the Hole"},
        {85: "Ace in the Hole"},
        {86: "Ace in the Hole"},
        {87: "Ace in the Hole"},
        {88: "Ace in the Hole"},
        {89: "Ace in the Hole"},
        {90: "Ace in the Hole"},
        {91: "Ace in the Hole"},
        {92: "Ace in the Hole"},
        {93: "Ace in the Hole"},
        {94: "Ace in the Hole"},
        {95: "Ace in the Hole"},
        {96: "Ace in the Hole"},
        {97: "Ace in the Hole"},
        {98: "Ace in the Hole"}
    }

    def SelectPerks(self, in_seed, in_range):
        rand.seed(in_seed)
        generatedList = rand.sample(range(in_range-1),4)
        for x in range(0,3):
            value = generatedList[x]
            generatedList[x] = value + 1
        return generatedList

    def get_data(self):
        with open("roulette_userdata.json", 'r') as file:
            return json.loads(file.read())



    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 98)
    
        await ctx.send(f"{ctx.author} krijgt: {self.SurvivorPerks[generatedPerks[0]]} {self.SurvivorPerks[generatedPerks[1]]} {self.SurvivorPerks[generatedPerks[2]]} {self.SurvivorPerks[generatedPerks[3]]}")

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        await ctx.send(f"Under construction :)")

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
