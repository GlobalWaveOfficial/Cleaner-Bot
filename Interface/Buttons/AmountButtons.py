import aiosqlite
import discord
from discord.ui import View, button, Button

class AmountButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="amount_yes")
    async def amount_yes(self, interaction: discord.Interaction, button: Button):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT variable_3 FROM DataTransfer WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        await auditDB.execute(f"UPDATE DefaultAmount SET default_amount = {data[0]} WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"UPDATE DataTransfer SET variable_3 = NULL WHERE guild_id {interaction.guild.id}")
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Default amount replaced with `{data[0]}`.", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="amount_no")
    async def amount_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)