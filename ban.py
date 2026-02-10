import discord
from discord.ext import commands

OWNER_ID = 918628339663634492  # <-- replace with YOUR user ID

async def setup(bot):

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
        if member.id == OWNER_ID:
            return await ctx.send("😈 You are immune to bans.")

        if member == ctx.author:
            return await ctx.send("❌ You can't ban yourself.")

        await member.ban(reason=reason)
        await ctx.send(f"🔨 Banned {member.mention}")

    @ban.error
    async def ban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?ban @user [reason]`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Couldn't find that user.")

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def unban(ctx, user_id: int):
        user = await bot.fetch_user(user_id)
        await ctx.guild.unban(user)
        await ctx.send(f"✅ Unbanned {user}")

    @unban.error
    async def unban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?unban user_id`")
        elif isinstance(error, commands.BadArgument):
            await ctx.send("❌ Invalid user ID.")
