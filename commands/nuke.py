import aiosqlite
import datetime
import discord
from discord.ext import commands
from discord import app_commands
from Interface.Buttons.NukeButtons import NukeButtons

class Nuke(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="nuke", description="This is a dangerous command, your whole server will be wiped")
    async def nuke(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        async with self.bot.database.execute(f"SELECT timestamp, status FROM NukeCooldowns WHERE guild_id = {interaction.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            if interaction.user.id == interaction.guild.owner_id:
                embed=discord.Embed(
                    title="Server Nuke Command",
                    description="This command will completely wipe everything in your server except server members. Make sure that you are aware of what you are going to do, this action cannot be undone!\n\n**ARE YOU SURE ABOUT THIS?**",
                    color=discord.Color.magenta()
                )
                embed.set_footer(text="This command can be used once per 15 days.")
                embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")

                await interaction.followup.send(embed=embed, view=NukeButtons())
            else:
                await interaction.followup.send("<:error:954610357761105980> Huh? only **Server Owner** can invoke this command!")
        else:
            now_time = datetime.datetime.now()
            future_time = datetime.datetime.fromtimestamp(data[0])
            timeleft = future_time - now_time

            embed=discord.Embed(
                title="Server Nuke Command On Cooldown",
                description=f"You can't use this command at the moment, please try again after the cooldown.\n**Time Left:** {timeleft.days} days\n\n<:cleaner:954598059952734268> Please ask `{self.bot.application.owner.name}#{self.bot.application.owner.discriminator}` in **Cleaner** support, if you were eligible and really needy to use `/nuke` command again then we will reset it for you. 😉",
                color=discord.Color.magenta()
            )
            embed.set_footer(text="This command can be used once per 30 days.")
            embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")

            await interaction.followup.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Nuke(bot))