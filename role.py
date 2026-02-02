import discord
from discord.ext import commands

OWNER_ID = 918628339663634492  # <-- replace with YOUR user ID

async def setup(bot):

    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def role(ctx, role: discord.Role, member: discord.Member):
        if member.id == OWNER_ID:
            return await ctx.send("😈 You are immune to role changes.")

        if role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't manage that role.")

        await member.add_roles(role)
        await ctx.send(f"✅ Gave {member.mention} the {role.name} role.")

    @role.error
    async def role_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?role @role @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that role or user.")
