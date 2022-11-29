import aiosqlite
import discord
from discord.ui import View, button, Button
from discord import ButtonStyle
from Interface.Modals.ReportReplyModal import ReplyModal

class ReportButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Reply", style=ButtonStyle.green, custom_id="reply_button")
    async def reply_func(self, interaction: discord.Interaction, button: Button):
        role = interaction.guild.get_role(1004052000415162398)
        if role in interaction.user.roles:
            await interaction.response.send_modal(ReplyModal())
        else:
            await interaction.followup.send(content="<:error:954610357761105980> MissingPermissions, You aren't authorized to do that!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji="<:upvote:1026912667824312350>", custom_id="upvote_button")
    async def upvote_button(self, interaction: discord.Interaction, button: Button):
        database = await aiosqlite.connect("./Databases/data.db")
        await database.execute(f"UPDATE ReportsAndSuggestions SET upvotes = upvotes + 1 WHERE message_id = {interaction.message.id}")
        await database.commit()
        await interaction.followup.send(content="<:done:954610357727543346> Success!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji="<:downvote:1026912669812412437>", custom_id="downvote_button")
    async def downvote_button(self, interaction: discord.Interaction, button: Button):
        database = await aiosqlite.connect("./Databases/data.db")
        await database.execute(f"UPDATE ReportsAndSuggestions SET downvotes = downvotes + 1 WHERE message_id = {interaction.message.id}")
        await database.commit()
        await interaction.followup.send(content="<:done:954610357727543346> Success!", ephemeral=True)
    
    @button(style=ButtonStyle.red, emoji="✖", custom_id="delete_report")
    async def report_delete(self, interaction: discord.Interaction, button: Button):
        await interaction.response.defer()
        mod_role = interaction.guild.get_role(1004051984640389141)
        if mod_role in interaction.user.roles:
            database = await aiosqlite.connect("./Databases/data.db")
            await database.execute(f"DELETE FROM ReportsAndSuggestions WHERE message_id = {interaction.message.id}")
            await database.commit()
            await interaction.message.delete()
        else:
            await interaction.followup.send(content="<:error:954610357761105980> MissingPermissions, You aren't authorized to do that!", ephemeral=True)