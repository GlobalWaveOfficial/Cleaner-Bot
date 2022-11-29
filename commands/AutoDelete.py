import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands
from Interface.Buttons.AutoDeleteButtons import AutoDeleteButtons

class AutoDelete(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    autodelete = app_commands.Group(name="auto-delete", description="Configure automatic message deletion in your server")

    @autodelete.command(name="set", description="Enable automatic message deletion in your server, to keep your channels empty.")
    @app_commands.describe(channel="The channel where you want to enable automatic message deletion", duration="Time after the messages will be deleted. (i.e 5 min = 300 seconds)")
    @app_commands.choices(duration=[
        app_commands.Choice(name="1 Minute", value=60),
        app_commands.Choice(name="3 Minutes", value=180),
        app_commands.Choice(name="5 Minutes", value=300)
                
    ])
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def auto_del(self, interaction: discord.Interaction, channel: discord.TextChannel, duration: app_commands.Choice[int]):
        await interaction.response.defer(ephemeral=True)
        auditDB = await aiosqlite.connect("./Databases/data.db")
        
        if duration.value >= 60:
            minutes = duration.value%3600//60
            seconds = duration.value%3600%60%60
            time = f"{minutes} minutes and {seconds} seconds"
        
        if 60 > duration.value:
            seconds = duration.value%3600%60%60
            time = f"{seconds} seconds"

        async with auditDB.execute(f"SELECT channel_1, duration_1 FROM AutoDeleteChannels WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await auditDB.execute(f"INSERT INTO AutoDeleteChannels VALUES ({interaction.guild.id}, {channel.id}, {duration.value}, NULL, NULL, NULL, NULL)")
            await auditDB.commit()
            await interaction.followup.send(f"<:done:954610357727543346> Auto-delete has been enabled in {channel.mention} with {time}.")
        else:
            old_channel = interaction.guild.get_channel(data[0])
            if old_channel == channel:
                await interaction.followup.send(f"<:warn:954610357748510770> {channel.mention} has auto-delete working already!")
            else:
                await auditDB.execute(f"INSERT INTO DataTransfer VALUES ({interaction.guild.id}, {channel.id}, {duration.value}, NULL) ON CONFLICT (guild_id) DO UPDATE SET variable_1 = {channel.id}, variable_2 = {duration.value} WHERE guild_id = {interaction.guild.id}")
                await auditDB.commit()
                embed = discord.Embed(
                    title="Auto-delete is already enabled!",
                    description=f"Auto-delete is already enabled in {old_channel.mention}, would you like to replace it with {channel.mention}",
                    color=discord.Color.magenta()
                )
                await interaction.followup.send(embed=embed, view=AutoDeleteButtons())
    
    @auto_del.error
    async def auto_del_error(error, interaction: discord.Interaction):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Channels)** permission to do that!", ephemeral=True)
        else:
            raise Exception
    
    @autodelete.command(name="disable", description="Disable automatic message deletion.")
    @app_commands.checks.has_permissions(manage_channels=True)
    @app_commands.checks.bot_has_permissions(manage_channels=True)
    async def auto_del_disable(self, interaction: discord.Interaction):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT channel_1, duration_1 FROM AutoDeleteChannels WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await interaction.response.send_message("<:warn:954610357748510770> Auto-delete isn't configured in this server.", ephemeral=True)
        
        else:
            await auditDB.execute(f"DELETE FROM AutoDeleteChannels WHERE guild_id = {interaction.guild.id}")
            await auditDB.commit()
            await interaction.response.send_message("<:done:954610357727543346> Auto-delete has been disabled.", ephemeral=True)
    
    @auto_del_disable.error
    async def auto_del_disable_error(error, interaction: discord.Interaction):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Channels)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Channels)** permission to do that!", ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot):
    await bot.add_cog(
        AutoDelete(bot))