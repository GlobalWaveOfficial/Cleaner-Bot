import discord
from discord.ui import View, button, Button
from discord import ButtonStyle

class CategoryDeleteButtons(View):
    def __init__(self, category, channel_names):
        self.category = category
        self.channel_names = channel_names
        super().__init__(timeout=None)
    
    @button(label="Confirm", style=ButtonStyle.green, custom_id="category_delete_confirm_button")
    async def cat_del_confirm(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(description=f"**Deleting 📁{self.category.name}:**\nDeleting following channels\n```{self.channel_names}```\n<a:load:955160502135316520> **Processing**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=None)

        for channel in self.category.channels:
            await channel.delete()
        await self.category.delete()

        await interaction.edit_original_response(embed=discord.Embed(description=f"**Deleted 📁{self.category.name}:**\nDeleted channels\n```{self.channel_names}```\n<:done:954610357727543346> **Process Completed**", color=discord.Color.green()))
    
    @button(label="Deny", style=ButtonStyle.red, custom_id="category_delete_deny_button")
    async def cat_del_deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=discord.Embed(description=f"<:error:954610357761105980> **Process Denied**", color=discord.Color.red()), view=None)