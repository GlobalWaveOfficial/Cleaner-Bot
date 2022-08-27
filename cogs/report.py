import traceback
import discord
from discord import app_commands
from discord.ext import commands


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
        channel = interaction.client.get_channel(1004064539479916655)
        report_embed = discord.Embed(
            title=self.heading,
            description=self.report,
            color=discord.Color.magenta()
        )
        report_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        msg = await channel.send(embed=report_embed)
        await msg.add_reaction("<:yes:955173808355033088>")
        await msg.add_reaction("<:no:955173807998513222>")
        await interaction.response.send_message("<:thankyou:966151700018765835> Your report has been sent!", ephemeral=True)



    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:error:954610357761105980> Oops! Something went wrong.", ephemeral=True)

        traceback.print_tb(error.__traceback__)

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="report", description="Experiencing Issues? Report it to us!")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugReport())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Report(bot))