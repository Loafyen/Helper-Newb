import discord
from discord.ext import commands
from datetime import timedelta

OWNER_ID = 123456789012345678  # <-- replace with YOUR user ID

def is_owner_or_perm(**perms):
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True
        return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
    return commands.check(predicate)

async def setup(bot):

    @bot.command()
    @is_owner_or_perm(moderate_members=True)
    async def mute(ctx, member: discord.Member, minutes: int):
        if member.id == OWNER_ID:
            return await ctx.send("😈 You are immune to mutes.")

        if minutes <= 0:
            return await ctx.send("❌ Time must be greater than 0.")

        duration = timedelta(minutes=minutes)
        await member.timeout(duration, reason=f"Muted by {ctx.author}")
        await ctx.send(f"🔇 Muted {member.mention} for {minutes} minute(s).")

    @bot.command()
    @is_owner_or_perm(moderate_members=True)
    async def unmute(ctx, member: discord.Member):
        await member.timeout(None)
        await ctx.send(f"🔊 Unmuted {member.mention}")

    @mute.error
    async def mute_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?mute @user [minutes]`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Minutes must be a number.")
