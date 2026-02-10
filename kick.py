import discord
from discord.ext import commands

OWNER_ID = 918628339663634492  

def is_owner_or_perm(**perms):
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True
        return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
    return commands.check(predicate)

async def setup(bot):

    @bot.command()
    @is_owner_or_perm(kick_members=True)
    async def kick(ctx, member: discord.Member, *, reason=None):
        if member.id == OWNER_ID:
            return await ctx.send("no lmao")

        await member.kick(reason=reason)
        await ctx.send(f"👢 Kicked {member.mention}")

    @kick.error
    async def kick_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?kick @user [reason]`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that user.")
