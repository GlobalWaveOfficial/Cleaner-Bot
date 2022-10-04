import aiosqlite
import discord
import datetime
from discord import RawReactionActionEvent, app_commands
from discord.ext import commands
from discord.ui import button, View, Button

'''-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------< Buttons >-----------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

class AmountButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="amount_yes")
    async def amount_yes(self, interaction: discord.Interaction, button: Button):
        await auditDB.execute(f"UPDATE DefaultAmount SET default_amount = {amt} WHERE guild_id = {interaction.guild.id}")
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Default amount replaced with `{amt}`.", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="amount_no")
    async def amount_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)

class AuditButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="audit_yes")
    async def audit_yes(self, interaction: discord.Interaction, button: Button):
        await auditDB.execute(f"UPDATE AuditChannels SET channel_id = {chnl.id} WHERE guild_id = {interaction.guild.id}")
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Audit channel {prv_chnl.mention} replaced with {chnl.mention}.", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="audit_no")
    async def audit_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)

class ResetButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="reset_yes")
    async def reset_yes(self, interaction: discord.Interaction, button: Button):
        await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultAmount WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM BadwordFilter WHERE guild_id = {interaction.guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultPins WHERE guild_id = {interaction.guild.id}")
        
        await auditDB.commit()
        await interaction.response.edit_message(content=f"<:done:954610357727543346> Success!", embed=None, view=None)

    @button(label="No", style=discord.ButtonStyle.red, custom_id="reset_no")
    async def reset_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:error:954610357761105980> Request Denied", embed=None, view=None)

'''-----------------------------------------------------------------------------------------------------------------------------------------------------------------------
----------------------------------------------------------------------< Commands >----------------------------------------------------------------------------------------
--------------------------------------------------------------------------------------------------------------------------------------------------------------------------'''

class Audit(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global auditDB
        auditDB = await aiosqlite.connect("data.db")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS AuditChannels (guild_id, channel_id, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS DefaultAmount (guild_id, default_amount, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS BadwordFilter (guild_id, words, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS DefaultPins (guild_id, condition, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (guild_id, user_id, message_id, title, content, upvotes, downvotes, PRIMARY KEY (message_id))")
        
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------< Audit Commands >--------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    settings = app_commands.Group(name="settings", description="shows the bot settings for the current server")

    @settings.command(name="default_pins", description="Assign a default pin deletion check, either Keep or Delete")
    @app_commands.describe()
    @app_commands.choices(default=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def pins(self, interaction: discord.Interaction, default: app_commands.Choice[str]):
        async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()

        if default.value == "delete":
            if data is None:
                await auditDB.execute(f"INSERT INTO DefaultPins VALUES ({interaction.guild.id}, 'delete')")
                await interaction.response.send_message(content="<:done:954610357727543346> Default pins check condition is set to **Delete**, your pinned messages will be deleted.", ephemeral=True)
                await auditDB.commit()
            else:
                await auditDB.execute(f"UPDATE DefaultPins SET condition = 'delete' WHERE guild_id = {interaction.guild.id}")
                await interaction.response.send_message(content="<:done:954610357727543346> Default pins check condition has been updated to **Delete**, your pinned messages will be deleted.", ephemeral=True)
                await auditDB.commit()
        
        if default.value == "keep":
            if data is None:
                await auditDB.execute(f"INSERT INTO DefaultPins VALUES ({interaction.guild.id}, 'keep')")
                await interaction.response.send_message(content="<:done:954610357727543346> Default pins check condition is set to **Keep**, now your pinned messages won't be deleted.", ephemeral=True)
                await auditDB.commit()
            else:
                await auditDB.execute(f"UPDATE DefaultPins SET condition = 'keep' WHERE guild_id = {interaction.guild.id}")
                await interaction.response.send_message(content="<:done:954610357727543346> Default pins check condition has been updated to **Keep**, now your pinned messages won't be deleted.", ephemeral=True)
                await auditDB.commit()

    @settings.command(name="audit_channel", description="Assign a channel for Message logs")
    @app_commands.describe(channel="The channel where you want get the logs.")
    @app_commands.checks.has_permissions(administrator=True)
    async def audit(self, interaction: discord.Interaction, channel: discord.TextChannel):
        global chnl
        chnl = channel
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            try:
                await auditDB.execute(f"INSERT INTO AuditChannels VALUES ({interaction.guild.id}, {channel.id})")
                await interaction.followup.send(f"<:done:954610357727543346> Successfully assigned {channel.mention} for Message Logs.")
                await channel.send(f"**{interaction.user}** has set this channel for Message Logs.")
                await auditDB.commit()
            except discord.errors.Forbidden:
                await interaction.followup.send(f"<:error:954610357761105980> Sorry, I'm unable to send messages in {channel.mention}.")
        
        if data[0] == chnl.id:
            await interaction.followup.send("<:error:954610357761105980> The mentioned channel is already assigned for audit logging")

        else:
            global prv_chnl
            prv_chnl = self.bot.get_channel(data[0])
            embed = discord.Embed(
                title="Old Audit Channel Detected!",
                description="I've noticed that, an audit channel for this server is already set. Would you like to replace it with new one?",
                color= discord.Color.magenta()
            )
            await interaction.followup.send(embed=embed, view=AuditButtons(), ephemeral=True)
    
    @audit.error
    async def audit_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)

    @settings.command(name="default_amount", description="Change default message cleaning amount")
    @app_commands.describe(amount="The amount you want to set as default cleaning amount.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_amount(self, interaction: discord.Interaction, amount: int):
        global amt
        amt = amount
        await interaction.response.defer(ephemeral=True)
        if amount > 100:
            await interaction.followup.send(content="<:error:954610357761105980> Default amount can't be greater than `100`!")
            return
        if amount == 0:
            await interaction.followup.send(content="<:error:954610357761105980> Default amount can't be zero!")
        if amount < 0:
            await interaction.followup.send(content="<:error:954610357761105980> Default amount can't lower than zero!")
        else:
            async with auditDB.execute(f"SELECT default_amount FROM DefaultAmount WHERE guild_id = {interaction.guild.id}") as cursor:
                data = await cursor.fetchone()
            if data is None:
                await auditDB.execute(f"INSERT INTO DefaultAmount VALUES ({interaction.guild.id}, {amount})")
                await interaction.followup.send(f"<:done:954610357727543346> Default cleaning amount is now set to `{amount}`")
                await auditDB.commit()
            
            if data[0] == amount:
                await interaction.followup.send(f"<:error:954610357761105980> Default cleaning amount is already set to `{amount}`")
                
            else:
                embed = discord.Embed(
                    title="Default Amount Detected!",
                    description=f"I've noticed that, a default amount for this server is already set to `{data[0]}`. Would you like to replace it with `{amount}`?",
                    color= discord.Color.magenta()
                )
                await interaction.followup.send(embed=embed, view=AmountButtons(), ephemeral=True)
    
    @set_amount.error
    async def set_amount_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------< Settings Commands >-----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @settings.command(name="reset", description="This command will reset every variable set in Cleaner#8788")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="⚠️ Warning",
            color=discord.Color.magenta(),
            description="<:warn:954610357748510770> This command will reset all the settings for this server!\nAre you sure about this?"
        ), view=ResetButtons(), ephemeral=True)
    
    @reset.error
    async def reset_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
    
    @settings.command(name="show", description="Shows the current bot configuration for the current server")
    @app_commands.checks.has_permissions(administrator=True)
    async def show(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {interaction.guild.id}") as cursor:
            badword_data = await cursor.fetchone()
        if badword_data is None:
            badword_data = "Nill"
        else:
            badword_data = badword_data[0].split(",")
        
        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {interaction.guild.id}") as cursor2:
            audit_data = await cursor2.fetchone()
        if audit_data is None:
            audit_data = "Nill"
        else:
            audit_data = self.bot.get_channel(audit_data[0]).mention
        
        async with auditDB.execute(f"SELECT default_amount FROM DefaultAmount WHERE guild_id = {interaction.guild.id}") as cursor3:
            amount_data = await cursor3.fetchone()
        if amount_data is None:
            amount_data = "5 (Not Configured)"
        else:
            amount_data = amount_data[0]
        
        async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
            pins_data = await cursor.fetchone()
        if pins_data is None:
            pins_data = "Nill"
        else:
            pins_data = str(pins_data[0]).capitalize()
        
        badwords = ""
        index = 0
        
        if badword_data != "Nill":
            for word in badword_data:
                index += 1
                badwords += f"{index}. {word}\n"
        else:
            badwords = "Nill"

        embed = discord.Embed(
            title=f"Cleaner Configuration for {interaction.guild.name}",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")
        embed.add_field(name="Audit Channel", value=f"{audit_data}", inline=False)
        embed.add_field(name="Default Cleaning Amount", value=f"{amount_data}", inline=False)
        embed.add_field(name="Default Pins Condition", value=f"{pins_data}", inline=False)
        embed.add_field(name="Blacklisted Words", value=badwords, inline=False)

        await interaction.followup.send(embed=embed)
    
    @show.error
    async def show_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------< BadWords Commands >-----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    bad_words = app_commands.Group(name="badwords", description="Add or remove bad words for the current words")

    @bad_words.command(name="add", description="blacklist a word, to prevent users from saying it")
    @app_commands.describe(word="The word you want to blacklist.")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def add(self, interaction: discord.Interaction, word:str):
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

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------< Autoclean Commands >----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------


#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#----------------------------------------------------------------------< Message Events >----------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        try:
            async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {message.channel.guild.id}") as cursor1:
                data = await cursor1.fetchone()
            if data is None:
                pass
            else:
                try:
                    words = data[0].split(",")
                    for word in words:
                        if word in message.content:
                            await message.delete()
                except:
                    word = data[0]
                    if word in message.content:
                        await message.delete()
        except:
            pass

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.author.bot:
            return
        Time = datetime.datetime.now()
        UpTime = Time.strftime("%d-%m-%Y %H:%M:%S")

        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {message.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            channel = self.bot.get_channel(data[0])
            await channel.send(embed= discord.Embed(title="Message Deleted!", description= f"<:time:954610357576548444> **Time** `{UpTime}`\n<:author:954610357761081424> **Author** {message.author.mention}\n<:channel:954457643227942923> **Channel** {message.channel.mention}\n<:messages:954610357773684837> **Message Content:** {message.content}", color=discord.Color.magenta()))
    
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        Time = datetime.datetime.now()
        UpTime = Time.strftime("%d-%m-%Y %H:%M:%S")

        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {before.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            channel = self.bot.get_channel(data[0])
            await channel.send(embed= discord.Embed(title="Message Edited!", description= f"<:time:954610357576548444> **Time** `{UpTime}`\n<:author:954610357761081424> **Author** {before.author.mention}\n<:channel:954457643227942923> **Channel** {before.channel.mention}\n<:messages:954610357773684837> **Messages**\n**Original Message:** {before.content}\n**Edited Message:** {after.content}", color=discord.Color.magenta()))
    
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#------------------------------------------------------------------------< Reaction Event >------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    @app_commands.checks.has_permissions(manage_messages=True)
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.emoji.name == "🗑️":
            channel = self.bot.get_channel(payload.channel_id)
            message = await channel.fetch_message(payload.message_id)
            await message.delete()

#------------------------------------------------------------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------< Other Events >-------------------------------------------------------------------------------
#------------------------------------------------------------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {channel.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            if channel.id == data[0]:
                await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {channel.guild.id}")
                await auditDB.commit()
            else:
                pass
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultAmount WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM BadwordFilter WHERE guild_id = {guild.id}")
        await auditDB.commit()
        
async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Audit(bot))