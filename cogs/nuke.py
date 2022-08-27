import discord
from discord.ext import commands
from discord import app_commands
from discord.ui import button, View, Button

class NukeButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Yes", style=discord.ButtonStyle.green, custom_id="nuke_yes")
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def nuke_yes(self, interaction: discord.Interaction, button: Button):
        embed = discord.Embed(
            title="Confirm the Nuke",
            description="By pressing the confirm button, you are agreeing that:\n\n・**Channels** will be deleted\n・**Categories** will be deleted\n・**Roles** will be deleted\n\nYou can still deny this nuke....",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")

        await interaction.response.edit_message(content=None, embed=embed, view=NukeConfirm())
    
    @button(label="No", style=discord.ButtonStyle.red, custom_id="nuke_no")
    async def nuke_no(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:done:954610357727543346> Request Denied", embed=None, view=None)
    
class NukeConfirm(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Confirm", style=discord.ButtonStyle.green, custom_id="nuke_confirm")
    @app_commands.checks.bot_has_permissions(manage_channels=True, manage_roles=True)
    async def nuke_confirm(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:warn:954610357748510770> NUKE STARTED", embed=None, view=None)
        roles = []
        for channel in interaction.guild.channels:
            try:
                await channel.delete()
            except:
                pass
        for category in interaction.guild.categories:
            try:
                await category.delete()
            except:
                pass
        for role in interaction.guild.roles:
            try:
                await role.delete()
            except:
                if role.name == "@everyone":
                    pass
                else:
                    roles.append(role.mention)
                    pass
        
        role_list = ', '.join(roles)
        chnl = await interaction.guild.create_text_channel(name="✅ Nuke Successful")
        await chnl.send(embed=discord.Embed(
            title="Nuke Completed!",
            description=f"The following roles can't be deleted,\n{role_list}\n\nEither they are managed by some integrations or their position is higher than me in the role hierarchy.",
            color=discord.Color.magenta()
        ))
    
    @button(label="Deny", style=discord.ButtonStyle.red, custom_id="nuke_deny")
    async def nuke_deny(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content="<:done:954610357727543346> Request Denied", embed=None, view=None)

class Nuke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="nuke", description="This is a dangerous command, your whole server will be wiped")
    async def nuke(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        print(interaction.user.id)
        print(interaction.guild.owner_id)
        if interaction.user.id == interaction.guild.owner_id:
            embed=discord.Embed(
                title="Server Nuke Command",
                description="This command will completely wipe everything in your server except server members. Make sure that you are aware of what you are going to do, this action cannot be undone!\n\n**ARE YOU SURE ABOUT THIS?**",
                color=discord.Color.magenta()
            )
            embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")

            await interaction.followup.send(embed=embed, view=NukeButtons())
        else:
            await interaction.followup.send("<:error:954610357761105980> Huh? only **Server Owner** can invoke this command!")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Nuke(bot))