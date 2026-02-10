import discord
from discord.ext import commands

OWNER_ID = 918628339663634492  # me

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
        # Block others from touching owner
        if member.id == OWNER_ID and ctx.author.id != OWNER_ID:
            return await ctx.send("😈 You can't change my roles.")

        await member.add_roles(role)
        await ctx.send(f"✅ Gave {role.mention} to {member.mention}")

    @bot.command()
    @is_owner_or_perm(manage_roles=True)
    async def derole(ctx, role: discord.Role, member: discord.Member):
        # Block others from touching owner
        if member.id == OWNER_ID and ctx.author.id != OWNER_ID:
            return await ctx.send("😈 You can't change my roles.")

        await member.remove_roles(role)
        await ctx.send(f"❌ Removed {role.mention} from {member.mention}")

    @role.error
    async def role_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?role @role @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that role or user.")

    @derole.error
    async def derole_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?derole @role @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that role or user.")
