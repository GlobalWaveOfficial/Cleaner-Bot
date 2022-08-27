import discord
from discord import app_commands, ButtonStyle
from discord.ext import commands
from discord.ui import View, button, Button
from discord.app_commands import errors
from discord.app_commands.checks import has_permissions

class CategoryDeleteButtons(View):
    def __init__(self, category, channel_names):
        self.category = category
        self.channel_names = channel_names
        super().__init__(timeout=None)
    
    @button(label="Confirm", style=ButtonStyle.green, custom_id="category_delete_confirm_button")
    async def cat_del_confirm(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(description=f"**Deleting 📁{self.category.name}:**\nDeleting following channels\n```{self.channel_names}```\n<a:load:955160502135316520> **Processing**", color=discord.Color.green())
        await interaction.response.edit_message(embed=embed, view=None)

        for channel in self.category.channels:
            await channel.delete()
        await self.category.delete()

        await interaction.edit_original_response(embed=discord.Embed(description=f"**Deleted 📁{self.category.name}:**\nDeleted channels\n```{self.channel_names}```\n<:done:954610357727543346> **Process Completed**", color=discord.Color.green()))
    
    @button(label="Deny", style=ButtonStyle.red, custom_id="category_delete_deny_button")
    async def cat_del_deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(embed=discord.Embed(description=f"<:error:954610357761105980> **Process Denied**", color=discord.Color.red()), view=None)

class Delete(commands.Cog):
    def __init__(self, bot:commands.Bot) -> None:
        self.bot = bot

    delete_group = app_commands.Group(name="delete", description="Delete unnecassry channel or roles")

    @delete_group.command(name="channel", description="Delete unnecessary channels")
    @app_commands.describe(channel="The channel you want to delete.")
    @has_permissions(manage_channels=True)
    async def channel(self, interaction: discord.Interaction, channel: discord.TextChannel):
        await channel.delete()
        await interaction.response.send_message(content=f"<:clean:954611061577896006> Deleted **#{channel}**", ephemeral=True)
        
    @channel.error
    async def channel_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Channels) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, errors.CommandInvokeError):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Channels) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception
        
    @delete_group.command(name="thread", description="Delete unnecessary thread")
    @app_commands.describe(thread="The thread you want to delete.")
    @has_permissions(manage_threads=True)
    async def thread(self, interaction: discord.Interaction, thread: discord.Thread):
        await thread.delete()
        await interaction.response.send_message(content=f"<:clean:954611061577896006> Deleted **#{thread}**", ephemeral=True)
        
    @thread.error
    async def thread_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Threads) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, errors.CommandInvokeError):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Threads) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

    @delete_group.command(name="role", description="Delete unnecessary roles")
    @app_commands.describe(role="The role you want to delete.")
    @has_permissions(manage_roles=True)
    async def role(self, interaction: discord.Interaction, role: discord.Role):
        await role.delete()
        await interaction.response.send_message(content=f"<:clean:954611061577896006> Deleted **{role}**", ephemeral=True)
        
    @role.error
    async def role_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Roles) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, errors.CommandInvokeError):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Roles) permission to process this command.", color=discord.Color.red()), ephemeral=True)
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
        if isinstance(error, errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Nicknames) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, errors.CommandInvokeError):
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
        if isinstance(error, errors.MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Manage Emojis and Stickers) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        if isinstance(error, errors.CommandInvokeError):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, I'm missing (Manage Emojis and Stickers) permission to process this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

    @delete_group.command(name="category", description="Delete unwanted categories including their channels.")
    @app_commands.describe(category="The category you want to delete.")
    @has_permissions(manage_channels=True)
    async def category_cmd(self, interaction: discord.Interaction, category: discord.CategoryChannel):
        await interaction.response.defer(ephemeral=True)
        index = 0
        channel_names = ""
        for channel in category.channels:
            index += 1
            channel_names += f"{index}. {channel.name}\n"
        
        embed = discord.Embed(description=f"**Deleting 📁{category.name}:**\nFollowing channels will be deleted\n```{channel_names}```\n<:warn:954610357748510770> **Confirmation Required**", color=discord.Color.orange())
        embed.set_footer(text="This action can't be reversed! Confirm at your own risk")

        await interaction.followup.send(embed=embed, view=CategoryDeleteButtons(category, channel_names))

    
async def setup(bot: commands.Cog) -> None:
    await bot.add_cog(
        Delete(bot))
