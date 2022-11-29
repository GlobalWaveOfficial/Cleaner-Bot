import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class Audit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    bad_words = app_commands.Group(name="badwords", description="Add or remove bad words for the current words")

    @bad_words.command(name="add", description="blacklist a word, to prevent users from saying it")
    @app_commands.describe(word="The word you want to blacklist.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, word:str):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await auditDB.execute(f"INSERT INTO BadwordFilter VALUES ({interaction.guild.id}, '{word}')")
            await auditDB.commit()
            await interaction.followup.send(f"<:done:954610357727543346> Added `{word}` to blacklisted words")
        else:
            words_string = ""
            words = data[0].split(",")
            words.append(word)
            for worrd in words:
                words_string += f"{worrd},"

            words_to_add = words_string[:-1]
            await auditDB.execute(f"UPDATE BadwordFilter SET words = '{words_to_add}' WHERE guild_id = {interaction.guild.id}")
            await auditDB.commit()
            await interaction.followup.send(f"<:done:954610357727543346> Added `{word}` to blacklisted words")
    
    @add.error
    async def add_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        
    @bad_words.command(name="remove", description="remove a blacklisted word")
    @app_commands.describe(word="The word you want to remove from blacklist.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def remove(self, interaction: discord.Interaction, word:str):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await interaction.followup.send("<:warn:954610357748510770> The provided word can't be found in blacklisted words")
        else:
            len_words = 0
            string_words = ""
            words = data[0].split(',')

            for i in words:
                if i == word:
                    words.remove(word)
                if word != i:
                    await interaction.followup.send(f"<:warn:954610357748510770> `{word}` isn't blacklisted!")
                    return
            
            for x in words:
                len_words += 1
                string_words += f"{x},"
            
            words_to_add = string_words[:-1]
            if len_words == 0:
                await auditDB.execute(f"DELETE FROM BadwordFilter WHERE guild_id = {interaction.guild.id}")
                await auditDB.commit()
                await interaction.followup.send(f"<:done:954610357727543346> Removed `{word}` from blacklisted words.")
            if len_words > 0:
                await auditDB.execute(f"UPDATE BadwordFilter SET words = '{words_to_add}' WHERE guild_id = {interaction.guild.id}")
                await auditDB.commit()
                await interaction.followup.send(f"<:done:954610357727543346> Removed `{word}` from blacklisted words.")
    
    @remove.error
    async def remove_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
    
    @bad_words.command(name="list", description="List the blacklisted words for your server")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def word_list(self, interaction: discord.Interaction):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await interaction.followup.send("<:warn:954610357748510770> There aren't any blacklisted words for this server.")
        else:
            count = 0
            words = data[0].split(",")
            word_list = ""

            for word in words:
                count += 1
                word_list += f"{word}\n"
            
            embed = discord.Embed(
                title=f"Blacklisted Words for {interaction.guild.name}",
                color=discord.Color.magenta()
            )
            embed.description = f"```\n{word_list}```\nTotal Blacklisted Words `{count}`"
            embed.set_thumbnail(url=interaction.guild.icon.url)
            embed.set_footer(text="Add or Remove badwords by /badwords add, /badwords remove")
            
            await interaction.followup.send(embed=embed)
    
    @word_list.error
    async def word_list_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Audit(bot))