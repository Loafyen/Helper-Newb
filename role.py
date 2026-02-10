import discord
from discord.ext import commands

OWNER_ID = 123456789012345678  # <-- replace with YOUR user ID

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
        # If target is owner but author is not owner -> block
        if member.id == OWNER_ID and ctx.author.id != OWNER_ID:
            return await ctx.send("😈 You can't change my roles.")

        # If author is owner targeting self -> allow
        await member.add_roles(role)
        await ctx.send(f"✅ Gave {role.mention} to {member.mention}")

    @role.error
    async def role_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?role @role @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that role or user.")
