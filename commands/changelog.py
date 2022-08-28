import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands
from discord.ui import View, button, Button
import config

embed = discord.Embed(
    colour=discord.Color.magenta()
)

embed.set_author(name='Last Updated on August 3, 2022', icon_url='https://i.imgur.com/T12D7JH.png')
embed.set_thumbnail(url='https://i.imgur.com/T12D7JH.png')
embed.add_field(name="Delete Command Updated", value="Delete command has two new options now,\n1. Emoji\n2. Nickname\nDo /help delete to see more information", inline=False)
embed.add_field(name="Pinned Message Exclusion", value="Now you can exclude pinned messages from deletion in clean command", inline=False)
embed.add_field(name="Tweaked Overall Experience", value="Updated commands, help, info. /set audit and /set amount is now /settings audit_channel and /settings default_amount.")
embed.add_field(name="Added Permissions Check", value="Now you can check for missing permissions. There will be a button when running permission check command which lets you re-invite the bot without kicking it from the server.")
embed.set_footer(text=f'v{config.BOT_VERSION} | type /report to send bug reports to us')

class Buttons(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label = "Here", style=discord.ButtonStyle.green, custom_id="help_yes")
    async def help_yes(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=None, embed=embed, view=None)
    
    @button(label = "DMs", style=discord.ButtonStyle.blurple, custom_id="help_no")
    async def help_no(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.user.send(embed=embed)
            await interaction.response.edit_message(content="<:done:954610357727543346> Check your DMs", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="<:error:954610357761105980> Your DMs are closed!", embed=None, view=None)

class ButtonsWithNotif(View):
    def __init__(self):
        super().__init__(timeout=None)

    @button(label = "Here", style=discord.ButtonStyle.green, custom_id="help_yes")
    async def help_yes(self, interaction: discord.Interaction, button: Button):
        await interaction.response.edit_message(content=None, embed=embed, view=None)
    
    @button(label = "DMs", style=discord.ButtonStyle.blurple, custom_id="help_no")
    async def help_no(self, interaction: discord.Interaction, button: Button):
        try:
            await interaction.user.send(embed=embed)
            await interaction.response.edit_message(content="<:done:954610357727543346> Check your DMs", embed=None, view=None)
        except:
            await interaction.response.edit_message(content="<:error:954610357761105980> Your DMs are closed!", embed=None, view=None)
    
    @button(label="View Notification", style=discord.ButtonStyle.red, emoji="<:notif:1013118962873147432>", custom_id="help_notif", row=2)
    async def help_notif(self, interaction: discord.Interaction, button: Button):
        database = await aiosqlite.connect("data.db")
        embed = discord.Embed(
            title="Latest Message | August 27, 2022",
            description="**Subject:** 🎉 Celebrating 2k Servers!\n\n<:cleaner:954598059952734268> **Cleaner#8788** is reaching 2000 servers, keeping them clean and providing quality services. On September 3rd, 2022 we are going to have live stream on our Stage Channel in [Cleaner's Support Server](https://discord.gg/QrFEfNuC5m). Make sure to join us, I (Developer X) will be there to answer your questions and also we may play some games together 😉. So yeah stay tuned with us!\n\nRegards,\n*Developer X#0001*"
        )
        await database.execute(f"INSERT INTO NotificationView VALUES ({interaction.user.id}, 'viewed') ON CONFLICT (user_id) DO UPDATE SET status = 'viewed' WHERE user_id = {interaction.user.id}")
        await interaction.response.edit_message(content="<:done:954610357727543346> **Notification Viewed**", embed=embed, view=None)
        await database.commit()
        await database.close()

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog", description="See what's new")
    async def changelog(self, interaction: discord.Interaction):
        database = await aiosqlite.connect("data.db")
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
            await interaction.response.send_message(content="<:notif:1013118962873147432> **You have an unread notification!**", embed=resp_embed, view=ButtonsWithNotif(), ephemeral=True)
            await database.close()
        else:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=Buttons(), ephemeral=True)
            await database.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Changelog(bot))
