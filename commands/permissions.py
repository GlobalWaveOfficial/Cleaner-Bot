import discord
from discord import app_commands
from discord.app_commands.errors import MissingPermissions
from discord.ext import commands
from discord.ui import View, Button
import config

class PermissionUpdateButton(View):
    def __init__(self):
        super().__init__(timeout=None)

        self.add_item(Button(label="Re-Invite", url="https://discord.com/api/oauth2/authorize?client_id=831223247357607968&permissions=430973479952&scope=bot%20applications.commands"))

class Permissions(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="check_permissions", description="Check if the bot has all required permissions.")
    @app_commands.checks.has_permissions(administrator=True)
    async def perm_check(self, interaction: discord.Interaction):
        await interaction.response.send_message("<a:load:955160502135316520> Initiating Permission Check", ephemeral=True)
        me = interaction.guild.get_member(831223247357607968)
        manage_roles = "<:error:954610357761105980> Manage Roles"
        manage_channels = "<:error:954610357761105980> Manage Channels"
        manage_nicknames = "<:error:954610357761105980> Manage Nicknames"
        manage_emojis_and_stickers = "<:error:954610357761105980> Manage Emojis and Stickers"
        read_messages = "<:error:954610357761105980> Read Messages"
        send_messages = "<:error:954610357761105980> Send Messages"
        send_messages_in_threads = "<:error:954610357761105980> Send Messages in Threads"
        manage_messages = "<:error:954610357761105980> Manage Messages"
        manage_threads = "<:error:954610357761105980> Manage Threads"
        embed_links = "<:error:954610357761105980> Embed Links"
        read_message_history = "<:error:954610357761105980> Read Message History"
        use_external_emojis = "<:error:954610357761105980> Use External Emojis"
        use_external_stickers = "<:error:954610357761105980> Use External Stickers"
        counter = 0
        if me.guild_permissions.manage_roles:
            manage_roles = "<:done:954610357727543346> Manage Roles"
            counter += 1
        if me.guild_permissions.manage_channels:
            manage_channels = "<:done:954610357727543346> Manage Channels"
            counter += 1
        if me.guild_permissions.manage_nicknames:
            manage_nicknames = "<:done:954610357727543346> Manage Nicknames"
            counter += 1
        if me.guild_permissions.manage_emojis_and_stickers:
            manage_emojis_and_stickers = "<:done:954610357727543346> Manage Emojis and Stickers"
            counter += 1
        if me.guild_permissions.read_messages:
            read_messages = "<:done:954610357727543346> Read Messages"
            counter += 1
        if me.guild_permissions.send_messages:
            send_messages = "<:done:954610357727543346> Send Messages"
            counter += 1
        if me.guild_permissions.send_messages_in_threads:
            send_messages_in_threads = "<:done:954610357727543346> Send Messages in Threads"
            counter += 1
        if me.guild_permissions.manage_messages:
            manage_messages = "<:done:954610357727543346> Manage Messages"
            counter += 1
        if me.guild_permissions.manage_threads:
            manage_threads = "<:done:954610357727543346> Manage Threads"
            counter += 1
        if me.guild_permissions.embed_links:
            embed_links = "<:done:954610357727543346> Embed Links"
            counter += 1
        if me.guild_permissions.read_message_history:
            read_message_history = "<:done:954610357727543346> Read Message History"
            counter += 1
        if me.guild_permissions.use_external_emojis:
            use_external_emojis = "<:done:954610357727543346>  Use External Emojis"
            counter += 1
        if me.guild_permissions.use_external_stickers:
            use_external_stickers = "<:done:954610357727543346> Use External Stickers"
            counter += 1
        
        if counter == 13:
            embed = discord.Embed(
                title="Permission Check Report",
                description=f"{manage_roles}\n{manage_channels}\n{manage_nicknames}\n{manage_emojis_and_stickers}\n{read_messages}\n{send_messages}\n{send_messages_in_threads}\n{manage_messages}\n{manage_threads}\n{embed_links}\n{read_message_history}\n{use_external_emojis}\n{use_external_stickers}\n\n<:done:954610357727543346> All permissions are granted!",
                color=discord.Color.magenta()
            )
            embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.edit_original_response(content=None, embed=embed)
        
        if counter != 13:
            embed = discord.Embed(
                title="Permission Check Report",
                description=f"{manage_roles}\n{manage_channels}\n{manage_nicknames}\n{manage_emojis_and_stickers}\n{read_messages}\n{send_messages}\n{send_messages_in_threads}\n{manage_messages}\n{manage_threads}\n{embed_links}\n{read_message_history}\n{use_external_emojis}\n{use_external_stickers}\n\n<:warn:954610357748510770> Missing permissions found!",
                color=discord.Color.magenta()
            )
            embed.set_thumbnail(url=interaction.guild.icon.url)
            embed.set_footer(text="Click the button below, to re-invite the bot without kicking")
            await interaction.edit_original_response(content=None, embed=embed, view=PermissionUpdateButton())
    
    @perm_check.error
    async def perm_chec_error(self, interaction: discord.Interaction, error: app_commands.AppCommandError):
        if isinstance(error, MissingPermissions):
            await interaction.response.send_message(embed=discord.Embed(description="<:error:954610357761105980> Missing Permissions, you are missing (Administrator) permission to invoke this command.", color=discord.Color.red()), ephemeral=True)
        else:
            raise Exception

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Permissions(bot))

#self.bot.application_info()
