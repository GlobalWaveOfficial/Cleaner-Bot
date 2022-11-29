import traceback
import aiosqlite
import discord
from Interface.Buttons.ReportButtons import ReportButtons

class BugReport(discord.ui.Modal, title="Report"):
    heading = discord.ui.TextInput(
        label="Title of your report",
        style=discord.TextStyle.short,
        placeholder="Type the title of your report, i.e Commands not working",
        required=True,
        max_length=30
    )

    report = discord.ui.TextInput(
        label="Tell us what you want to report",
        style=discord.TextStyle.long,
        placeholder="Describe your issue in detail",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        channel = interaction.client.get_channel(1004064457204437152)
        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.report,
            color=discord.Color.magenta()
        )
        suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        suggestion_embed.set_thumbnail(url=interaction.guild.icon.url)
        suggestion_embed.set_footer(text=f"Sent from, Guild: {interaction.guild.name} | Members: {interaction.guild.member_count}")

        msg = await channel.send(embed=suggestion_embed, view=ReportButtons())
        await auditDB.execute(f'INSERT INTO ReportsAndSuggestions VALUES ({interaction.guild.id}, {interaction.user.id}, {msg.id}, "{self.heading}", "{self.report}", 0, 0)')
        await interaction.response.send_message("<:thankyou:966151700018765835> Your report has been sent!", ephemeral=True)
        await auditDB.commit()
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:error:954610357761105980> Oops! Something went wrong.", ephemeral=True)

        traceback.print_tb(error.__traceback__)