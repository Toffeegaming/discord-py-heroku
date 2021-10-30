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

    # SurvivorPerks = [
    #     {"id": 1,"name": "Ace in the Hole"},
    #     {"id": 2,"name": "Adrenaline"},
    #     {"id": 3,"name": "Aftercare"},
    #     {"id": 4,"name": "Alert"},
    #     {"id": 5,"name": "Any Means Necessary"},
    #     {"id": 6,"name": "Appraisal"},
    #     {"id": 7,"name": "Autodidact"},
    #     {"id": 8,"name": "Balanced Landing"},
    #     {"id": 9,"name": "Bite the Bullet"},
    #     {"id": 10,"name": "Ace in the Hole"}, ######################## https://deadbydaylight.fandom.com/wiki/Perks
    #     {"id": 11,"name": "Ace in the Hole"},
    #     {"id": 12,"name": "Ace in the Hole"},
    #     {"id": 13,"name": "Ace in the Hole"},
    #     {"id": 14,"name": "Ace in the Hole"},
    #     {"id": 15,"name": "Ace in the Hole"},
    #     {"id": 16,"name": "Ace in the Hole"},
    #     {"id": 17,"name": "Ace in the Hole"},
    #     {"id": 18,"name": "Ace in the Hole"},
    #     {"id": 19,"name": "Ace in the Hole"},
    #     {"id": 20,"name": "Ace in the Hole"},
    #     {"id": 21,"name": "Ace in the Hole"},
    #     {"id": 22,"name": "Ace in the Hole"},
    #     {"id": 23,"name": "Ace in the Hole"},
    #     {"id": 24,"name": "Ace in the Hole"},
    #     {"id": 25,"name": "Ace in the Hole"},
    #     {"id": 26,"name": "Ace in the Hole"},
    #     {"id": 27,"name": "Ace in the Hole"},
    #     {"id": 28,"name": "Ace in the Hole"},
    #     {"id": 29,"name": "Ace in the Hole"},
    #     {"id": 30,"name": "Ace in the Hole"},
    #     {"id": 31,"name": "Ace in the Hole"},
    #     {"id": 32,"name": "Ace in the Hole"},
    #     {"id": 33,"name": "Ace in the Hole"},
    #     {"id": 34,"name": "Ace in the Hole"},
    #     {"id": 35,"name": "Ace in the Hole"},
    #     {"id": 36,"name": "Ace in the Hole"},
    #     {"id": 37,"name": "Ace in the Hole"},
    #     {"id": 38,"name": "Ace in the Hole"},
    #     {"id": 39,"name": "Ace in the Hole"},
    #     {"id": 40,"name": "Ace in the Hole"},
    #     {"id": 41,"name": "Ace in the Hole"},
    #     {"id": 42,"name": "Ace in the Hole"},
    #     {"id": 43,"name": "Ace in the Hole"},
    #     {"id": 44,"name": "Ace in the Hole"},
    #     {"id": 45,"name": "Ace in the Hole"},
    #     {"id": 46,"name": "Ace in the Hole"},
    #     {"id": 47,"name": "Ace in the Hole"},
    #     {"id": 48,"name": "Ace in the Hole"},
    #     {"id": 49,"name": "Ace in the Hole"},
    #     {"id": 50,"name": "Ace in the Hole"},
    #     {"id": 51,"name": "Ace in the Hole"},
    #     {"id": 52,"name": "Ace in the Hole"},
    #     {"id": 53,"name": "Ace in the Hole"},
    #     {"id": 54,"name": "Ace in the Hole"},
    #     {"id": 55,"name": "Ace in the Hole"},
    #     {"id": 56,"name": "Ace in the Hole"},
    #     {"id": 57,"name": "Ace in the Hole"},
    #     {"id": 58,"name": "Ace in the Hole"},
    #     {"id": 59,"name": "Ace in the Hole"},
    #     {"id": 60,"name": "Ace in the Hole"},
    #     {"id": 61,"name": "Ace in the Hole"},
    #     {"id": 62,"name": "Ace in the Hole"},
    #     {"id": 63,"name": "Ace in the Hole"},
    #     {"id": 64,"name": "Ace in the Hole"},
    #     {"id": 65,"name": "Ace in the Hole"},
    #     {"id": 66,"name": "Ace in the Hole"},
    #     {"id": 67,"name": "Ace in the Hole"},
    #     {"id": 68,"name": "Ace in the Hole"},
    #     {"id": 69,"name": "Ace in the Hole"},
    #     {"id": 70,"name": "Ace in the Hole"},
    #     {"id": 71,"name": "Ace in the Hole"},
    #     {"id": 72,"name": "Ace in the Hole"},
    #     {"id": 73,"name": "Ace in the Hole"},
    #     {"id": 74,"name": "Ace in the Hole"},
    #     {"id": 75,"name": "Ace in the Hole"},
    #     {"id": 76,"name": "Ace in the Hole"},
    #     {"id": 77,"name": "Ace in the Hole"},
    #     {"id": 78,"name": "Ace in the Hole"},
    #     {"id": 79,"name": "Ace in the Hole"},
    #     {"id": 80,"name": "Ace in the Hole"},
    #     {"id": 81,"name": "Ace in the Hole"},
    #     {"id": 82,"name": "Ace in the Hole"},
    #     {"id": 83,"name": "Ace in the Hole"},
    #     {"id": 84,"name": "Ace in the Hole"},
    #     {"id": 85,"name": "Ace in the Hole"},
    #     {"id": 86,"name": "Ace in the Hole"},
    #     {"id": 87,"name": "Ace in the Hole"},
    #     {"id": 88,"name": "Ace in the Hole"},
    #     {"id": 89,"name": "Ace in the Hole"},
    #     {"id": 90,"name": "Ace in the Hole"},
    #     {"id": 91,"name": "Ace in the Hole"},
    #     {"id": 92,"name": "Ace in the Hole"},
    #     {"id": 93,"name": "Ace in the Hole"},
    #     {"id": 94,"name": "Ace in the Hole"},
    #     {"id": 95,"name": "Ace in the Hole"},
    #     {"id": 96,"name": "Ace in the Hole"},
    #     {"id": 97,"name": "Ace in the Hole"},
    #     {"id": 98,"name": "Ace in the Hole"}
    #     ]

    def SelectPerks(self, in_seed, in_range):
        rand.seed(in_seed)
        generatedList = rand.sample(range(in_range-1),4)
        print(generatedList)
        for x in generatedList:
            value = generatedList[x]
            generatedList[x] = value + 1
        return generatedList

    def get_data(self):
        with open("roulette_userdata.json", 'r') as file:
            return json.loads(file.read())



    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 98)
        await ctx.send(f"Your perks are: {generatedPerks[0]} {generatedPerks[1]}  {generatedPerks[2]} {generatedPerks[3]}")

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        await ctx.send(f"Under construction :)")

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
