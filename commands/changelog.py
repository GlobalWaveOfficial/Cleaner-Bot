import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from discord.ui import View, button, Button
import config

embed = discord.Embed(
    colour=discord.Color.magenta()
)

embed.set_author(name='Last Updated on October 5, 2022', icon_url='https://i.imgur.com/T12D7JH.png')
embed.set_thumbnail(url='https://i.imgur.com/T12D7JH.png')
embed.add_field(name="Pinned Message Condition is Optional", value="Now the pinned message check condition option is optional and by default it is set to **Delete**, you can change its value by `/settings default_pins` command.", inline=False)
embed.add_field(name="New Settings Command Added", value="Added command in settings group called `default_pins`. Now you can set either to delete pins or keep them without selecting it everytime.", inline=False)
embed.add_field(name="Added Category Delete", value="Now you can delete a whole category including channels, `/delete category`", inline=False)
embed.add_field(name="Stay Updated", value="Now you can receive latest messages by us, the notification will be shown under `/help` and `/changelog` commands.", inline=False)
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
    
    @button(label="View Notification", style=discord.ButtonStyle.red, emoji="<:notif:1013118962873147432>", custom_id="help_notif")
    async def help_notif(self, interaction: discord.Interaction, button: Button):
        database = await aiosqlite.connect("data.db")
        embed = discord.Embed(
            title="Latest Message | August 27, 2022",
            description="**Subject:** 🎉 Celebrating 2k Servers!\n\n<:cleaner:954598059952734268> **Cleaner#8788** is reaching 2000 servers, keeping them clean and providing quality services. On September 3rd, 2022 we are going to have live stream on our Stage Channel in [Cleaner's Support Server](https://discord.gg/QrFEfNuC5m). Make sure to join us, I (Developer X) will be there to answer your questions and also we may play some games together 😉. So yeah stay tuned with us!\n\nRegards,\n*Developer X#0001*",
            color=discord.Color.magenta()
        )
        embed.set_thumbnail(url=interaction.client.user.avatar.url)
        embed.set_footer(text="You can view this message again by using /news")
        await database.execute(f"INSERT INTO NotificationView VALUES ({interaction.user.id}, 'viewed') ON CONFLICT (user_id) DO UPDATE SET status = 'viewed' WHERE user_id = {interaction.user.id}")
        await interaction.response.edit_message(content="<:done:954610357727543346> **Notification Viewed**", embed=embed, view=None)
        await database.commit()
        await database.close()

class Changelog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="changelog", description="See what's new")
    async def help(self, interaction: discord.Interaction):
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
                title="Where do you want to receive the changelog?",
                description="Here? or in DMs?",
                color=discord.Color.magenta()
            )
            resp_embed.set_footer(text=f"Cleaner#8788 v{config.BOT_VERSION}")
            await interaction.response.send_message(embed=resp_embed, view=Buttons(), ephemeral=True)
            await database.close()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        Changelog(bot))