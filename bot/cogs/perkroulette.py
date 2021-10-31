import os
from discord.ext.commands import Bot, Cog
from discord_slash import cog_ext, SlashContext

import discord
import json
import requests

from discord_slash.utils.manage_commands import generate_options

guild_ids = [int(os.getenv("GUILD2")), int(os.getenv("GUILD3"))]



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

    ######### https://deadbydaylight.fandom.com/wiki/Perks
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

    def get_data(self):
        with open("roulette_userdata.json", 'r') as file:
            return json.loads(file.read())

    @cog_ext.cog_slash(name='Survivor', description='Krijg 4 random survivor perks!', guild_ids=guild_ids)
    async def _Survivor(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 97)
        embed = discord.Embed(
            title="",
            description=f"{ctx.author.name} krijgt:{os.linesep}{self.SurvivorPerks[generatedPerks[0]]}{os.linesep}{self.SurvivorPerks[generatedPerks[1]]}{os.linesep}{self.SurvivorPerks[generatedPerks[2]]}{os.linesep}{self.SurvivorPerks[generatedPerks[3]]}",
            color=int(0x9628f7,16))
        embed.set_footer(text="Gebruik de command opnieuw voor andere perks!")
        await ctx.send(embed=embed)

    @cog_ext.cog_slash(name='Killer', description='Krijg 4 random killer perks!', guild_ids=guild_ids)
    async def _Killer(self,ctx: SlashContext):
        generatedPerks = self.SelectPerks(ctx.author_id, 86)
        await ctx.send()
        embed = discord.Embed(
            title="",
            description=f"{ctx.author.name} krijgt:{os.linesep}{self.KillerPerks[generatedPerks[0]]}{os.linesep}{self.KillerPerks[generatedPerks[1]]}{os.linesep}{self.KillerPerks[generatedPerks[2]]}{os.linesep}{self.KillerPerks[generatedPerks[3]]}",
            color=int(0x9628f7,16))
        embed.set_footer(text="Gebruik de command opnieuw voor andere perks!")
        await ctx.send(embed=embed)
        print(f"{self.KillerPerks[86]}")
        print(f"{self.KillerPerks[87]}")

def setup(bot: Bot):
    bot.add_cog( Roulette(bot) )
