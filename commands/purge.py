import asyncio
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import button, View, Button

class CategoryButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="category_purge_yes")
    async def category_purge_yes(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=f"<:clean:954611061577896006> Cleaning **{interaction.channel.category.name.upper()}**", view=None)
        no_of_channels = len(interaction.channel.category.channels)
        deleted_channels = 0
        for channel in interaction.channel.category.channels:
            await channel.delete()
            deleted_channels += 1
            await channel.clone()

            if deleted_channels == no_of_channels:
                old_category = await interaction.channel.category
                old_category_name = old_category.name()
                new_category = await interaction.guild.create_category(name=old_category_name)
                for channel in interaction.channel.category.channels:
                    await channel.move(category=new_category, beginning=True)
                
                await old_category.delete()
    
    @button(label="No", style=discord.ButtonStyle.red, custom_id="category_purge_no")
    async def category_purge_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", view=None)

class Purge(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    purge_group = app_commands.Group(name="purge", description="re-create channel or a whole category of channels")

    @purge_group.command(name="channel", description="Recreates current or mentioned channel")
    @app_commands.describe(channel="The channel you want to re-create.")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel=None):
        if channel is None:
            await interaction.response.defer()
            try:
                await interaction.followup.send(f"<:warn:954610357748510770> {interaction.user.mention} has initiated a <:nuke:954611061745655868> **Nuke!**")
                await asyncio.sleep(5)
                await interaction.channel.send(f"<:blast:954631464102813736> Nuking.....")
                position = interaction.channel.position
                await interaction.channel.delete(reason=f"{interaction.user} invoked Purge command")
                chnl = await interaction.channel.clone(reason=f"{interaction.user} invoked Purge command")
                await chnl.move(category=interaction.channel.category, beginning=True, offset=position)

            except discord.errors.Forbidden:
                await interaction.followup.send("<:error:954610357761105980> Sorry, I don't have **(Manage Channels)** permission to do that!")
        else:
            await interaction.response.defer(ephemeral=True)
            try:
                await interaction.followup.send("<:blast:954631464102813736> The mentioned channel will be nuked in a while")
                await channel.send(f"<:warn:954610357748510770> {interaction.user.mention} has initiated a <:nuke:954611061745655868> **Nuke!**")
                await asyncio.sleep(5)
                await channel.send(f"<:blast:954631464102813736> Nuking.....")
                position = channel.position
                await channel.delete(reason=f"{interaction.user} invoked Purge command")
                chnl = await channel.clone(reason=f"{interaction.user} invoked Purge command")
                await chnl.move(category=interaction.channel.category, beginning=True, offset=position)
                await interaction.edit_original_message(content="<:done:954610357727543346> Nuke Successful")

            except discord.errors.Forbidden:
                await interaction.followup.send("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!")
    
    @channel.error
    async def channel_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)
    
    @purge_group.command(name="category", description="Recreates current")
    @app_commands.checks.has_permissions(manage_channels=True)
    async def category(self, interaction: discord.Interaction):
        old_category = interaction.channel.category.id
        global cat
        cat = self.bot.get_channel(old_category)
        await interaction.response.send_message(f"<:warn:954610357748510770> This command will re-create the current category.\nAre you sure about this?", ephemeral=True, view=CategoryButtons())
    
    @category.error
    async def category_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Purge(bot))
