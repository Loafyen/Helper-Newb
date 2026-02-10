import discord
from discord.ext import commands

log_channel_id = None

async def setup(bot):

    @bot.command()
    @commands.has_permissions(administrator=True)
    async def logs(ctx):
        global log_channel_id
        log_channel_id = ctx.channel.id
        await ctx.send("✅ This channel is now the logs channel.")

    @bot.event
    async def on_message_delete(message):
        global log_channel_id
        if not log_channel_id or message.author.bot:
            return

        channel = bot.get_channel(log_channel_id)
        if not channel:
            return

        embed = discord.Embed(
            title="🗑️ Message Deleted",
            description=message.content or "*No text content*",
            color=discord.Color.red()
        )
        embed.add_field(name="Author", value=message.author.mention)
        embed.add_field(name="Channel", value=message.channel.mention)
        await channel.send(embed=embed)
