import discord
from discord.ext import commands

TICKET_CATEGORY_NAME = "Tickets"
SUPPORT_ROLE_NAME = "Mod"  # change if needed

class TicketView(discord.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @discord.ui.button(label="🎫 Open Ticket", style=discord.ButtonStyle.green)
    async def open_ticket(self, interaction: discord.Interaction, button: discord.ui.Button):
        guild = interaction.guild
        user = interaction.user

        category = discord.utils.get(guild.categories, name=TICKET_CATEGORY_NAME)
        if not category:
            category = await guild.create_category(TICKET_CATEGORY_NAME)

        overwrites = {
            guild.default_role: discord.PermissionOverwrite(view_channel=False),
            user: discord.PermissionOverwrite(view_channel=True, send_messages=True),
        }

        support_role = discord.utils.get(guild.roles, name=SUPPORT_ROLE_NAME)
        if support_role:
            overwrites[support_role] = discord.PermissionOverwrite(view_channel=True, send_messages=True)

        channel = await guild.create_text_channel(
            name=f"ticket-{user.name}",
            category=category,
            overwrites=overwrites
        )

        await channel.send(f"{user.mention} Welcome! A moderator will help you shortly.")
        await interaction.response.send_message("✅ Ticket created!", ephemeral=True)

async def setup(bot):
    @bot.command()
    @commands.has_permissions(administrator=True)
    async def ticket(ctx):
        embed = discord.Embed(
            title="Support Tickets",
            description="Click the button below to open a ticket.",
            color=discord.Color.green()
        )
        await ctx.send(embed=embed, view=TicketView())
