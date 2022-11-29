import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands
from Interface.Buttons.ResetButtons import ResetButtons
from Interface.Buttons.AuditButtons import AuditButtons
from Interface.Buttons.AmountButtons import AmountButtons

class Settings(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot

    settings = app_commands.Group(name="settings", description="shows the bot settings for the current server")

    @settings.command(name="default-pins", description="Assign a default pin deletion check, either Keep or Delete")
    @app_commands.describe()
    @app_commands.choices(default=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(administrator=True)
    async def pins(self, interaction: discord.Interaction, default: app_commands.Choice[str]):
        auditDB = await aiosqlite.connect("./Databases/data.db")
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

    @settings.command(name="audit-channel", description="Assign a channel for Message logs")
    @app_commands.describe(channel="The channel where you want get the logs.")
    @app_commands.checks.has_permissions(administrator=True)
    async def audit(self, interaction: discord.Interaction, channel: discord.TextChannel):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await auditDB.execute(f"INSERT INTO DataTransfer VALUES ({interaction.guild.id}, {channel.id}, NULL, NULL) ON CONFLICT (guild_id) DO UPDATE SET variable_1 = {channel.id} WHERE guild_id = {interaction.guild.id}")
        await auditDB.commit()
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
                raise Exception
        
        if data[0] == channel.id:
            await interaction.followup.send("<:error:954610357761105980> The mentioned channel is already assigned for audit logging")

        else:
            prv_chnl = interaction.guild.get_channel(data[0])
            await auditDB.execute(f"INSERT INTO DataTransfer VALUES ({interaction.guild.id}, NULL, {prv_chnl.id}, NULL) ON CONFLICT (guild_id) DO UPDATE SET variable_2 = {prv_chnl.id} WHERE guild_id = {interaction.guild.id}")
            await auditDB.commit()
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
        else:
            raise Exception

    @settings.command(name="default-amount", description="Change default message cleaning amount")
    @app_commands.describe(amount="The amount you want to set as default cleaning amount.")
    @app_commands.checks.has_permissions(administrator=True)
    async def set_amount(self, interaction: discord.Interaction, amount: int):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        amt = amount
        await auditDB.execute(f"INSERT INTO DataTransfer VALUES ({interaction.guild.id}, NULL, NULL, {amt}) ON CONFLICT (guild_id) DO UPDATE SET variable_3 = {amt} WHERE guild_id = {interaction.guild.id}")
        await auditDB.commit()
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
        else:
            raise Exception

    @settings.command(name="reset", description="This command will reset every variable set in Cleaner#8788")
    @app_commands.checks.has_permissions(administrator=True)
    async def reset(self, interaction: discord.Interaction):
        await interaction.response.send_message(embed=discord.Embed(
            title="⚠️ Settings Reset Warning!",
            color=discord.Color.magenta(),
            description="<:warn:954610357748510770> This command will reset all the settings for this server!\nAre you sure about this?"
        ), view=ResetButtons(), ephemeral=True)
    
    @reset.error
    async def reset_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
        else:
            raise Exception

    @settings.command(name="show", description="Shows the current bot configuration for the current server")
    @app_commands.checks.has_permissions(administrator=True)
    async def show(self, interaction: discord.Interaction):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await interaction.response.defer(ephemeral=True)
        async with auditDB.execute(f"SELECT channel_1, duration_1 FROM AutoDeleteChannels WHERE guild_id = {interaction.guild.id}") as cursor:
            autodel_data = await cursor.fetchone()
        if autodel_data is None:
            autodel_data = "Not Configured\n`/settings auto-delete <channel>`"
        else:
            autodel_data_channel = interaction.guild.get_channel(autodel_data[0])
            duration = autodel_data[1]
            if duration >= 60:
                minutes = duration%3600//60
                seconds = duration%3600%60%60
                time = f"{minutes} minutes and {seconds} seconds"
            
            if 60 > duration:
                seconds = duration%3600%60%60
                time = f"{seconds} seconds"
            
            autodel_data = f"Channel: {autodel_data_channel.mention}\nDuration: {time}"

        async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {interaction.guild.id}") as cursor1:
            data = await cursor1.fetchone()
        if data is None:
            badword_data = "Not Configured\n`/badwords add <word>`"
        else:
            badword_data = data[0].split(",")
        
        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {interaction.guild.id}") as cursor2:
            audit_data = await cursor2.fetchone()
        if audit_data is None:
            audit_data = "Not Configured\n`/settings audit-channel <channel>`"
        else:
            audit_data = self.bot.get_channel(audit_data[0]).mention
        
        async with auditDB.execute(f"SELECT default_amount FROM DefaultAmount WHERE guild_id = {interaction.guild.id}") as cursor3:
            amount_data = await cursor3.fetchone()
        if amount_data is None:
            amount_data = "5 (Not Configured)\n`/settings default-amount <amount>`"
        else:
            amount_data = amount_data[0]
        
        async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
            pins_data = await cursor.fetchone()
        if pins_data is None:
            pins_data = "Not Configured\n`/settings default-pins <condition>`"
        else:
            pins_data = str(pins_data[0]).capitalize()
        
        badwords = ""
        index = 0
        
        if badword_data != "Not Configured\n`/badwords add <word>`":
            for word in badword_data:
                index += 1
                badwords += f"{index}. {word}\n"
        else:
            badwords = "Not Configured\n`/badwords add <word>`"

        embed = discord.Embed(
            title=f"Cleaner Configuration for {interaction.guild.name}",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")
        embed.add_field(name="Audit Channel", value=f"{audit_data}", inline=False)
        embed.add_field(name="Auto-Delete", value=f"{autodel_data}", inline=False)
        embed.add_field(name="Default Cleaning Amount", value=f"{amount_data}", inline=False)
        embed.add_field(name="Default Pins Condition", value=f"{pins_data}", inline=False)
        embed.add_field(name="Blacklisted Words", value=badwords, inline=False)
        embed.set_image(url="https://i.imgur.com/a4p0eDE.png")

        await interaction.followup.send(embed=embed)
    
    @show.error
    async def show_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Administrator)** permissions to do that!", ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Settings(bot))