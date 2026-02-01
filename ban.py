import discord
from discord.ext import commands

async def setup(bot):

    @bot.command()
    @commands.has_permissions(ban_members=True)
    async def ban(ctx, member: discord.Member, *, reason=None):
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
    async def unban(ctx, *, user):
        banned_users = [entry async for entry in ctx.guild.bans()]
        name, discriminator = user.split("#")

        for entry in banned_users:
            if (entry.user.name, entry.user.discriminator) == (name, discriminator):
                await ctx.guild.unban(entry.user)
                await ctx.send(f"✅ Unbanned {entry.user.name}#{entry.user.discriminator}")
                return

        await ctx.send("❌ User not found in ban list.")

    @unban.error
    async def unban_error(ctx, error):
        if isinstance(error, commands.MissingPermissions):
            await ctx.send("❌ You don't have permission to use this.")
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send("❌ Usage: `?unban username#1234`")
