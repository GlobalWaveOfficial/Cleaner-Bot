import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class Clean(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    clean_group = app_commands.Group(name="clean", description="Message cleaning related commands")

    @clean_group.command(name="messages", description="Clean 0-100 number of messages from the current channel")
    @app_commands.describe(pins="Choose either you want to keep the pins or not.", amount="Amount of messages you want to delete, default 5", contains="Delete those messages which contain certain phrases or keywords.")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def clear(self, interaction: discord.Interaction, pins: app_commands.Choice[str]=None, amount: int=None, contains: str=None):
        await interaction.response.defer(ephemeral=True)
        auditDB = await aiosqlite.connect("./Databases/data.db")
        if contains is None:
            def contain_check(message: discord.Message):
                return message

        if contains is not None:
            def contain_check(message: discord.Message):
                return contains in message.content

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

        if pins is None:
            async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
                data2 = await cursor.fetchone()
            if data2 is None:
                deleted = await interaction.channel.purge(limit=amount, check=contain_check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return

            if data2[0] == "delete":
                deleted = await interaction.channel.purge(limit=amount, check=contain_check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return

            if data2[0] == "keep":
                counter = 0
                pins = await interaction.channel.pins()
                for i in pins:
                    counter += 1
                def check(message: discord.Message):
                    return message.pinned == False

                deleted = await interaction.channel.purge(limit=amount+counter, check=check and contain_check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return
            return

        elif pins.value == "keep":
            pins = await interaction.channel.pins()
            for i in pins:
                counter += 1
            def check(message: discord.Message):
                return message.pinned == False

            deleted = await interaction.channel.purge(limit=amount+counter, check=check and contain_check)
            await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
            return

        elif pins.value == "delete":
            deleted = await interaction.channel.purge(limit=amount, check=contain_check)
            await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
            return

    @clear.error
    async def clean_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            raise Exception
    
    @clean_group.command(name="mass-delete", description="Deletes someone's message all across the server, regardless of other parameters.")
    @app_commands.describe(user="The member who's messages you want to delete.")
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def mass_delete(self, interaction: discord.Interaction, user: discord.Member):
        await interaction.response.defer(ephemeral=True)
        
        def user_check(message: discord.Message):
            return message.author == user
        
        counter = 0
        for channel in interaction.guild.text_channels:
            try:
                deleted = await channel.purge(check=user_check)
            except:
                pass
            counter += len(deleted)
        
        await interaction.followup.send(f"<:clean:954611061577896006> All messages sent my {user.mention} are deleted.", ephemeral=True)
    
    @mass_delete.error
    async def mass_delete_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            raise Exception
    
    @clean_group.command(name="user", description="Delete 0-100 messages sent by a specific user from the current channel")
    @app_commands.describe(user="The member who's messages you want to delete.", pins="Choose either you want to keep the pins or not.", amount="Amount of messages you want to delete, default 5", contains="Delete those messages which contain certain phrases or keywords.")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def uc(self, interaction: discord.Interaction, user: discord.Member, pins: app_commands.Choice[str]=None, amount: int=None, contains: str=None):
        await interaction.response.defer(ephemeral=True)
        auditDB = await aiosqlite.connect("./Databases/data.db")
        if contains is None:
            def contain_check(message: discord.Message):
                return message

        if contains is not None:
            def contain_check(message: discord.Message):
                return contains in message.content

        if user.bot:
            await interaction.followup.send("<:warn:954610357748510770> Please use `/clean bot` for **Bots**!")
            return

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

        def user_check(message: discord.Message):
            return message.author == user

        if pins is None:
            async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
                data2 = await cursor.fetchone()
            if data2 is None:
                    deleted = await interaction.channel.purge(limit=amount, check=user_check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return

            if data2[0] == "delete":
                    deleted = await interaction.channel.purge(limit=amount, check=user_check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return
            

            if data2[0] == "keep":
                    counter = 0
                    pins = await interaction.channel.pins()
                    for i in pins:
                        counter += 1
                    def check(message: discord.Message):
                        return message.pinned == False

                    deleted = await interaction.channel.purge(limit=amount+counter, check=user_check and check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return
            
            return

        elif pins.value == "keep":
                pins = await interaction.channel.pins()
                for i in pins:
                    counter += 1
                def check(message: discord.Message):
                    return message.pinned == False

                deleted = await interaction.channel.purge(limit=amount+counter, check=user_check and check and contain_check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return

        elif pins.value == "delete":
                deleted = await interaction.channel.purge(limit=amount)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return
    
    @uc.error
    async def uc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            raise Exception

    @clean_group.command(name="bot", description="Delete 0-100 messages sent by bots from the current channel")
    @app_commands.describe(bot="The bot who's messages you want to delete.", pins="Choose either you want to keep the pins or not.", amount="Amount of messages you want to delete, default 5", contains="Delete those messages which contain certain phrases or keywords.")
    @app_commands.choices(pins=[
        app_commands.Choice(name="Delete", value="delete"),
        app_commands.Choice(name="Keep", value="keep")
    ])
    @app_commands.checks.has_permissions(manage_messages=True)
    @app_commands.checks.bot_has_permissions(manage_messages=True)
    async def bc(self, interaction: discord.Interaction, bot: discord.Member=None, pins: app_commands.Choice[str]=None, amount:int=None, contains: str=None):
        await interaction.response.defer(ephemeral=True)
        auditDB = await aiosqlite.connect("./Databases/data.db")
        if contains is None:
            def contain_check(message: discord.Message):
                return message

        if contains is not None:
            def contain_check(message: discord.Message):
                return contains in message.content

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
        
        if bot is None:
            def user_check(message: discord.Message):
                return message.author == discord.Member.bot

        if bot is not None:
            if not bot.bot:
                await interaction.followup.send("<:warn:954610357748510770> This command is only supported for bots!")
                return

            def user_check(message: discord.Message):
                return message.author == bot

        if pins is None:
            async with auditDB.execute(f"SELECT condition FROM DefaultPins WHERE guild_id = {interaction.guild.id}") as cursor:
                data2 = await cursor.fetchone()
            if data2 is None:
                    deleted = await interaction.channel.purge(limit=amount, check=user_check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return
            

            if data2[0] == "delete":
                    deleted = await interaction.channel.purge(limit=amount, check=user_check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return
            

            if data2[0] == "keep":
                    counter = 0
                    pins = await interaction.channel.pins()
                    for i in pins:
                        counter += 1
                    def check(message: discord.Message):
                        return message.pinned == False

                    deleted = await interaction.channel.purge(limit=amount+counter, check=user_check and check and contain_check)
                    await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                    return
            

            return

        elif pins.value == "keep":
                pins = await interaction.channel.pins()
                for i in pins:
                    counter += 1
                def check(message: discord.Message):
                    return message.pinned == False

                deleted = await interaction.channel.purge(limit=amount+counter, check=user_check and check and contain_check)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return

        elif pins.value == "delete":
                deleted = await interaction.channel.purge(limit=amount)
                await interaction.followup.send(f"<:clean:954611061577896006> Deleted `{len(deleted)}/{amount}` messages.")
                return

    @bc.error
    async def bc_error(self, interaction: discord.Interaction, error):
        if isinstance(error, app_commands.errors.MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Messages)** permissions to do that!", ephemeral=True)
        if isinstance(error, app_commands.errors.BotMissingPermissions):
            await interaction.response.send_message("<:error:954610357761105980> Sorry, I don't have **(Manage Messages)** permission to do that!", ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Clean(bot))