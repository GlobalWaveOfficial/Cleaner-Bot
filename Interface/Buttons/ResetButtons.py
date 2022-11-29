import aiosqlite
import discord
from discord.ui import View, button, Button

class ResetButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="reset_yes")
    async def reset_yes(self, interaction: discord.Interaction, button: Button):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultAmount WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM BadwordFilter WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultPins WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM DataTransfer WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM AutoDeleteChannels WHERE guild_id = {interaction.guild.id}")
        
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Success!", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="reset_no")
    async def reset_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)