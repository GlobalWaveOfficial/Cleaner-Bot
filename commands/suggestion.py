import traceback
import discord
from discord import app_commands
from discord.ext import commands


class SubSuggestion(discord.ui.Modal, title="Suggestion"):
    heading = discord.ui.TextInput(
        label="Title of your suggestion",
        style=discord.TextStyle.short,
        placeholder="Type something catchy, for more upvotes ;)",
        required=True,
        max_length=30
    )

    suggestion = discord.ui.TextInput(
        label="Tell us what is in your brain",
        style=discord.TextStyle.long,
        placeholder="Suggest something unique ;)",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1004064457204437152)
        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.suggestion,
            color=discord.Color.magenta()
        )
        suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        msg = await channel.send(embed=suggestion_embed)
        await msg.add_reaction("<:yes:955173808355033088>")
        await msg.add_reaction("<:no:955173807998513222>")
        await interaction.response.send_message("<:thankyou:966151700018765835> Your suggestion has been recorded!", ephemeral=True)



    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:error:954610357761105980> Oops! Something went wrong.", ephemeral=True)

        traceback.print_tb(error.__traceback__)

class Suggest(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="suggestion", description="Got an Idea? share with us!")
    async def suggest(self, interaction: discord.Interaction):
        await interaction.response.send_modal(SubSuggestion())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Suggest(bot))