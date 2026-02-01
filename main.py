import discord
from discord.ext import commands
import os
from keep_alive import keep_alive

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    await bot.load_extension("tickets")
    await bot.load_extension("fun")
    await bot.load_extension("logs")

keep_alive()
bot.run(os.getenv("TOKEN"))
