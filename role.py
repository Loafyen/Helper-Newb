import discord
from discord.ext import commands

async def setup(bot):

    @bot.command()
    @commands.has_permissions(manage_roles=True)
    async def role(ctx, role: discord.Role, member: discord.Member):
        if member == ctx.author:
            return await ctx.send("❌ You can't give a role to yourself.")

        # Check if bot can manage the role
        if role >= ctx.guild.me.top_role:
            return await ctx.send("❌ I can't manage that role because it's higher than my highest role.")

        try:
            await member.add_roles(role)
            await ctx.send(f"✅ Gave {member.mention} the {role.name} role.")
        except discord.Forbidden:
            await ctx.send("❌ I don't have permission to add this role.")
        except Exception as e:
            await ctx.send(f"❌ An error occurred: {e}")

    @role.error
    async def role_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this command.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?role @role @user`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that role or user.")
