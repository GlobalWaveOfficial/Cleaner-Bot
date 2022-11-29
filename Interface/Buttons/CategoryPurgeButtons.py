import discord
from discord.ui import View, button, Button

class CategoryPurgeButtons(View):
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