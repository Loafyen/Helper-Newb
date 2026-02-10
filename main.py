import discord
from discord.ext import commands
import asyncio

OWNER_IDS = {123456789012345678, 987654321098765432}  # <-- PUT YOUR USER IDS HERE

intents = discord.Intents.default()
intents.message_content = True
intents.members = True
intents.moderation = True

bot = commands.Bot(command_prefix="?", intents=intents)

bot.OWNER_IDS = OWNER_IDS  # 👈 makes owners accessible in every file

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
bot.run("BOT_TOKEN")
