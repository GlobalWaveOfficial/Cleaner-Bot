import discord
import aiosqlite
import config

from discord import app_commands
from discord.ext import commands
from discord.ui import View, button, Button
from Interface.Buttons.ChangelogButtons import ChangelogButtons, ChangelogButtonsWithNotif

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog", description="See what's new")
    async def help(self, interaction: discord.Interaction):
        database = await aiosqlite.connect("./Databases/data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS NotificationView (user_id, status, PRIMARY KEY (user_id))")
        async with database.execute(f"SELECT status FROM NotificationView WHERE user_id = {interaction.user.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            resp_embed = discord.Embed(
                title="Where do you want to receive the changelog?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(content="<:notif:1013118962873147432> **You have an unread notification!**", embed=resp_embed, view=ChangelogButtonsWithNotif(), ephemeral=True)
        else:
            resp_embed = discord.Embed(
                title="Where do you want to receive the changelog?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=ChangelogButtons(), ephemeral=True)

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Changelog(bot))