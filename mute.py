import discord
from discord.ext import commands
from datetime import timedelta

async def setup(bot):

    def is_owner_or_perm(**perms):
        async def predicate(ctx):
            if ctx.author.id in bot.OWNER_IDS:
                return True
            return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
        return commands.check(predicate)

    @bot.command()
    @is_owner_or_perm(moderate_members=True)
    async def mute(ctx, member: discord.Member, minutes: int):
        if member.id in bot.OWNER_IDS:
            return await ctx.send("😈 That user is immune.")

        if minutes <= 0:
            return await ctx.send("❌ Time must be positive.")

        await member.timeout(timedelta(minutes=minutes))
        await ctx.send(f"🔇 Muted {member.mention} for {minutes} minutes.")

    @bot.command()
    @is_owner_or_perm(moderate_members=True)
    async def unmute(ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 Unmuted {member.mention}")

    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Usage: ?mute @user minutes")
