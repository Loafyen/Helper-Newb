import discord
from discord.ext import commands

OWNER_ID = 918628339663634492  # <-- same ID

def is_owner_or_perm(**perms):
    async def predicate(ctx):
        if ctx.author.id == OWNER_ID:
            return True
        return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
    return commands.check(predicate)

async def setup(bot):

    @bot.command()
    @is_owner_or_perm(manage_roles=True)
    async def role(ctx, role: discord.Role, member: discord.Member):
        if member.id == OWNER_ID:
            return await ctx.send("😈 You are immune to role changes.")

        if role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't manage that role.")

        await member.add_roles(role)
        await ctx.send(f"✅ Gave {member.mention} the {role.name} role.")
