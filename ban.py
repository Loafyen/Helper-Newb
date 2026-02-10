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
    @is_owner_or_perm(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        if member.id == OWNER_ID:
            return await ctx.send("😈 You are immune to bans.")

        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member.mention}")

    @bot.command()
    @is_owner_or_perm(ban_members=True)
    async def unban(ctx, user_id: int):
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user}")
