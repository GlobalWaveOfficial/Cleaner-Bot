import aiosqlite
import discord
from discord import app_commands, RawReactionActionEvent
from discord.ext import commands


class Clean(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global auditDB
        auditDB = await aiosqlite.connect("data.db")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS AuditChannels (guild_id, channel_id, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS DefaultAmount (guild_id, default_amount, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS BadwordFilter (guild_id, words, PRIMARY KEY (guild_id))")

    clean_group = app_commands.Group(name="clean", description="Message cleaning related commands")

    @clean_group.command(name="messages", description="Clean 0-100 number of messages from the current channel")
    @app_commands.describe(pins="Choose either you want to keep the pins or not.", amount="Amound of messages you want to delete, default 5")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, pins: app_commands.Choice[str], amount: int=None):
        await interaction.response.defer(ephemeral=True)
        if amount is None:
            async with auditDB.execute(f"SELECT default_amount FROM DefaultAmount WHERE guild_id = {interaction.guild.id}") as cursor:
                data = await cursor.fetchone()
            if data is None:
                amount = 5
            else:
                amount = data[0]
        elif amount > 100:
            await interaction.followup.send("<:warn:954610357748510770> You can't delete more than 100 messages at once!")
            return
        elif amount == 0:
            await interaction.followup.send("<:warn:954610357748510770> No message will be deleted if amount is 0!")
            return
        try:
            if pins.value == "keep":
                def check(message: discord.Message):
                    return message.pinned == False

                deleted = await interaction.channel.purge(limit=amount, check=check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")

            if pins.value == "delete":
                deleted = await interaction.channel.purge(limit=amount)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
        except discord.errors.Forbidden:
            await interaction.followup.send("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!")

    @clear.error
    async def clean_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
    
    @clean_group.command(name="user", description="Delete 0-100 messages sent by a specific user from the current channel")
    @app_commands.describe(user="The member who's messages you want to delete.", amount="Amound of messages you want to delete, default 5")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def uc(self, interaction: discord.Interaction, user: discord.Member, amount:int=None):
        await interaction.response.defer(ephemeral=True)
        if user.bot:
            await interaction.followup.send("<:warn:954610357748510770> Why using this command when I have a separate command for Bots? use `/botclear` for **Bots**!")
            return
        if amount is None:
            amount = 5
        
        messages = [msg async for msg in interaction.channel.history(limit=100)]
        msgs = 0
        for msg in messages:
            if msg.author.id == user.id:
                try:
                    await msg.delete()
                    msgs += 1
                except discord.errors.Forbidden:
                    await interaction.followup.send("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!")
                    return
            
            if msgs == 5:
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **{user.name}**!")
                return
            elif msgs == amount:
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **{user.name}**!")
                return
        
        if msgs == 0:
            await interaction.followup.send("<:warn:954610357748510770> The **User** you've mentioned is inactive I think <:think:954627810243256390>, because I'm unable to find any message sent recently by him.")
            return
        else:
            await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **{user.name}**!")
            return
    
    @uc.error
    async def uc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)

    @clean_group.command(name="bot", description="Delete 0-100 messages sent by bots from the current channel")
    @app_commands.describe(amount="Amound of messages you want to delete, default 5")
    @app_commands.checks.has_permissions(manage_messages=True)
    async def bc(self, interaction: discord.Interaction, amount:int=None):
        await interaction.response.defer(ephemeral=True)
        if amount is None:
            amount = 5
        
        messages = [msg async for msg in interaction.channel.history(limit=100)]
        msgs = 0
        for msg in messages:
            if msg.author.bot:
                try:
                    await msg.delete()
                    msgs += 1
                except discord.errors.Forbidden:
                    await interaction.followup.send("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!")
                    return
            
            if msgs == 5:
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **Bots**!")
                return
            if msgs == amount:
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **Bots**!")
                return
        
        if msgs == 0:
            await interaction.followup.send("<:warn:954610357748510770> There are no **Bot** messages in recent 100 messages!")
            return
        else:
            await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{msgs}/{amount}` messages sent by **Bots**!")
            return

    @bc.error
    async def bc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload: RawReactionActionEvent):
        if payload.emoji.name == "🗑️":
            if payload.member.guild_permissions.manage_messages is True:
                channel = self.bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                await message.delete()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Clean(bot))