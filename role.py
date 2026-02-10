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
    @is_owner_or_perm(manage_roles=True)
    async def role(ctx, role: discord.Role, member: discord.Member):
        if member.id in bot.OWNER_IDS and ctx.author.id not in bot.OWNER_IDS:
            return await ctx.send("😈 You can't change that user's roles.")

        await member.add_roles(role)
        await ctx.send(f"✅ Gave {role.mention} to {member.mention}")

    @bot.command()
    @is_owner_or_perm(manage_roles=True)
    async def derole(ctx, role: discord.Role, member: discord.Member):
        if member.id in bot.OWNER_IDS and ctx.author.id not in bot.OWNER_IDS:
            return await ctx.send("😈 You can't change that user's roles.")

        await member.remove_roles(role)
        await ctx.send(f"❌ Removed {role.mention} from {member.mention}")

    @role.error
    async def role_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find role or user.")

    @derole.error
    async def derole_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission.")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find role or user.")
