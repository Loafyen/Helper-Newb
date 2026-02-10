import discord
from discord.ext import commands
import asyncio
import os
import sys

OWNER_IDS = {918628339663634492, 1424568124136624148}  # your IDs

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

token = os.getenv("DISCORD_TOKEN")
if not token:
    print("❌ DISCORD_TOKEN not found in environment. Exiting.")
    sys.exit(1)

bot.run(token)
