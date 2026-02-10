import discord
from discord.ext import commands

async def setup(bot):

    bot.log_channels = {}  # guild_id -> channel_id

    def is_owner_or_perm(**perms):
        async def predicate(ctx):
            if ctx.author.id in bot.OWNER_IDS:
                return True
            return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
        return commands.check(predicate)

    @bot.command()
    @is_owner_or_perm(administrator=True)
    async def logs(ctx):
        bot.log_channels[ctx.guild.id] = ctx.channel.id
        await ctx.send("📜 This channel is now the logs channel.")

    @bot.event
    async def on_message_delete(message):
        if not message.guild or message.author.bot:
            return

        channel_id = bot.log_channels.get(message.guild.id)
        if not channel_id:
            return

        log_channel = message.guild.get_channel(channel_id)
        if not log_channel:
            return

        embed = discord.Embed(title="🗑 Message Deleted", color=discord.Color.red())
        embed.add_field(name="Author", value=message.author.mention, inline=False)
        embed.add_field(name="Channel", value=message.channel.mention, inline=False)
        embed.add_field(name="Content", value=message.content or "*No text*", inline=False)

        await log_channel.send(embed=embed)
