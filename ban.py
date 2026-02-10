import discord
from discord.ext import commands

async def setup(bot):

    def is_owner_or_perm(**perms):
        async def predicate(ctx):
            if ctx.author.id in bot.OWNER_IDS:
                return True
            return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
        return commands.check(predicate)

    @bot.command()
    @is_owner_or_perm(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        if member.id in bot.OWNER_IDS:
            return await ctx.send("😈 That user is immune.")

        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member.mention}")

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ User not found.")
