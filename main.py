import discord
from discord.ext import commands
import asyncio
import os

OWNER_IDS = {918628339663634492, 1424568124136624148}  # <-- put your Discord user ID(s) here

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix="?", intents=intents)
bot.OWNER_IDS = OWNER_IDS

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load():
    await bot.load_extension("ban")
    await bot.load_extension("kick")
    await bot.load_extension("mute")
    await bot.load_extension("role")
    await bot.load_extension("tickets")
    await bot.load_extension("logs")

asyncio.run(load())

bot.run(os.environ["DISCORD_TOKEN"])
