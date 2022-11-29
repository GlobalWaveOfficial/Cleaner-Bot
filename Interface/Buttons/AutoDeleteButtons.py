import aiosqlite
import discord
from discord.ui import View, button, Button

class AutoDeleteButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="auto_yes")
    async def auto_yes(self, interaction: discord.Interaction, button: Button):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT variable_1, variable_2 FROM DataTransfer WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        channel = interaction.guild.get_channel(data[0])
        await auditDB.execute(f"UPDATE AutoDeleteChannels SET channel_1 = {data[0]}, duration_1 = {data[1]} WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"UPDATE DataTransfer SET variable_1 = NULL, variable_2 = NULL WHERE guild_id = {interaction.guild.id}")
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Auto-delete has been moved to {channel.mention}.", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="auto_no")
    async def auto_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)
