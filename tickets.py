import discord
from discord.ext import commands

async def setup(bot):

    def is_owner_or_perm(**perms):
        async def predicate(ctx):
            if ctx.author.id in bot.OWNER_IDS:
                return True
            return ctx.author.guild_permissions.is_superset(discord.Permissions(**perms))
        return commands.check(predicate)

    class TicketView(discord.ui.View):
        def __init__(self):
            super().__init__(timeout=None)

        @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.green)
        async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
            guild = interaction.guild
            user = interaction.user

            overwrites = {
                guild.default_role: discord.PermissionOverwrite(view_channel=False),
                user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
            }

            for role in guild.roles:
                if role.permissions.manage_messages:
                    overwrites[role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

            channel = await guild.create_text_channel(
                name=f"ticket-{user.name}",
                overwrites=overwrites
            )

            await interaction.response.send_message(f"🎟 Ticket created: {channel.mention}", ephemeral=True)

    @bot.command()
    @is_owner_or_perm(administrator=True)
    async def ticket(ctx):
        await ctx.send("Click the button below to open a ticket:", view=TicketView())
