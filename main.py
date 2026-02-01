import discord
from discord.ext import commands
import os

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load():
    await bot.load_extension("tickets")
    await bot.load_extension("logs")
    await bot.load_extension("fun")
    await bot.load_extension("ban")

bot.setup_hook = load

bot.run(os.getenv("TOKEN"))
