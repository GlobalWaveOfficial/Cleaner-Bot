import discord
from discord import app_commands
from discord.ext import commands
from discord.app_commands.errors import MissingPermissions, BotMissingPermissions
from discord.app_commands.checks import has_permissions

class Delete(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    delete_group = app_commands.Group(name="delete", description="Delete unnecassry channel or roles")

    @delete_group.command(name="channel", description="Delete unnecessary channels")
    @app_commands.describe(channel="The channel you want to delete.")
    @has_permissions(manage_channels=True)
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await channel.delete()
        await interaction.followup.send(f"<:clean:954611061577896006> Deleted **#{channel}**")
        
    @channel.error
    async def channel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Channels) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Channels) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        
    @delete_group.command(name="thread", description="Delete unnecessary thread")
    @app_commands.describe(thread="The thread you want to delete.")
    @has_permissions(manage_threads=True)
    async def thread(self, interaction: discord.Interaction, thread: discord.Thread):
        await thread.delete()
        await interaction.followup.send(f"<:clean:954611061577896006> Deleted **#{thread}**")
        
    @thread.error
    async def thread_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Threads) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Threads) permission to process this command.", color=discord.Color.red()), ephemeral=True)

    @delete_group.command(name="role", description="Delete unnecessary roles")
    @app_commands.describe(role="The role you want to delete.")
    @has_permissions(manage_roles=True)
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        await interaction.response.defer(ephemeral=True)
        await role.delete()
        await interaction.followup.send(f"<:clean:954611061577896006> Deleted **{role}**")
        await interaction.followup.send(f"<:error:954610357761105980> Sorry {interaction.user.mention}, I do not have the required **(Manage Roles)** permissions to do that!")
        
    @role.error
    async def role_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(f"<:error:954610357761105980> Sorry {interaction.user.mention}, you do not have the required **(Manage Roles)** permissions to do that!", ephemeral=True)
        else:
            raise Exception

    @delete_group.command(name="nickname", description="Delete/Reset someone's nickname to their default username.")
    @app_commands.describe(user="The user who's nickname you want to delete.")
    @has_permissions(manage_nicknames=True)
    async def nickname(self, interaction: discord.Interaction, user: discord.Member):
        nick = user.display_name
        name = user.name
        if nick == name:
            await interaction.response.send_message(f"<:warn:954610357748510770> Oops! {user.mention} doesn't have any nickname.", ephemeral=True)
        if nick != name:
            await user.edit(nick=None)
            await interaction.response.send_message(f"<:done:954610357727543346> Success! {user.mention}'s nickname has been removed.", ephemeral=True)
        
    @nickname.error
    async def nick_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Nicknames) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Nicknames) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception
    
    @delete_group.command(name="emoji", description="Delete unwanted emojis from the server.")
    @app_commands.describe(emoji="The emoji you want to delete.")
    @has_permissions(manage_emojis=True)
    async def emoji(self, interaction: discord.Interaction, emoji: str):
        try:
            emoji_id = discord.PartialEmoji.from_str(emoji).id
            if interaction.client.get_emoji(emoji_id).guild.id == interaction.guild.id:
                emoji = interaction.client.get_emoji(emoji_id)
                await emoji.delete()
                await interaction.response.send_message("<:done:954610357727543346> Success! The specified emoji has been deleted.", ephemeral=True)
            
            if interaction.client.get_emoji(emoji_id).guild.id != interaction.guild.id:
                await interaction.response.send_message("<:error:954610357761105980> Oops! The specified emoji doesn't belong to this server/guild.", ephemeral=True)
        except:
            await interaction.response.send_message("<:error:954610357761105980> Oops! I can't locate that emoji.", ephemeral=True)
    
    @emoji.error
    async def emoji_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Emojis and Stickers) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Emojis and Stickers) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

    @delete_group.command(name="category", description="Delete unwanted categories including their channels.")
    @app_commands.describe(category="The category you want to delete.")
    @has_permissions(manage_channels=True)
    async def category(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        await interaction.response.defer(ephemeral=True)
        index = 0
        channel_names = ""
        for channel in category.channels:
            index += 1
            channel_names += f"{index}. {channel.name}\n"
            await channel.delete(reason="Invoked Category Delete Command")
        await category.delete()

        embed = discord.Embed(description=f"<:done:954610357727543346> {category.name} has been deleted with following channels:\n{channel_names}", color=discord.Color.green())
        await interaction.followup.send(embed=embed)

    @category.error
    async def category_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Channels) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, BotMissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Channels) permission to process this command.", color=discord.Color.red()), ephemeral=True)



async def setup(bot: commands.Cog) -> None:
    await bot.add_cog(
        Delete(bot))
