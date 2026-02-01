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

@bot.command()
async def test(ctx):
    await ctx.send("hi")

# Load command files
async def load():
    await bot.load_extension("tickets")
    await bot.load_extension("logs")
    await bot.load_extension("fun")

bot.setup_hook = load

bot.run(os.getenv("TOKEN"))
