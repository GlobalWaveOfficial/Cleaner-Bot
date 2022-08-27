import discord
import aiosqlite
from discord import app_commands
from discord.ext import commands
from discord.ui import View, button, Button
import config

embed = discord.Embed(
    colour=discord.Color.magenta()
)

embed.set_author(name='Cleaner Bot Commands',icon_url='https://i.imgur.com/T12D7JH.png')
embed.set_thumbnail(url='https://i.imgur.com/T12D7JH.png')
embed.add_field(name='Help', value='Shows this message', inline=False)
embed.add_field(name="**__Cleaning Commands:__**", value="These commands can be found under /clean command group\n**Clean:** Delete a specified number of messages.\n**User:** Delete a specified of messages sent by the mentioned user.\n**Bot:** Delete a specified number of messages sent by bots.", inline=False)
embed.add_field(name="**__Delete Commands:__**", value="These commands can be found under /delete command group\n**Channel:** Delete the mentioned channel.\n**Category:** Delete the mentioned category.\n**Role:** Delete the mentioned role.\n**Thread:** Delete the mentioned thread.\n**Emoji:** Delete the specified emoji.\n**Nickname:** Delete the nickname of the mentioned user set in current server.", inline=False)
embed.add_field(name="**__Purge Commands:__**", value="These commands can be found under /purge command group\n**Channel:** Deletes and re-creates the mentioned or current channel, with same permissions.\n**Category:** Deletes and re-creates the current category", inline=False)
embed.add_field(name="**__Settings Commands:__**", value="These commands can be founf under /settings command group\n**Audit Channel:** Set a channel to get message logs.\n**Default Amount:** Set default cleaning amount for clean message command\n**Reset:** Reset all settings for the current server.\n**Show:** View the current settings for the server.", inline=False)
embed.add_field(name="**__Special Commands:__**", value="Following command can be invoked by server owner only.\n**Nuke:** Wipes everything from the server except members, THIS IS A DANGEROUS COMMAND!", inline=False)
embed.add_field(name="**__Help & Support:__**", value="**Report:** Facing issues using the bot? submit the report by /report\n**Suggestion:** Want something to get added to bot? Tell us your ideas /suggestion", inline=False)
embed.add_field(name="**__Other Commands:__**", value="**Check Permissions:** Check if the bot has all necessary permisions to work properly\n**Info** Show bot's information\n**Changelog:** Show latest changelog.\n**Ping:** Show bot's current latency.\n**Help:** Shows this message.", inline=False)
embed.set_footer(text=f'v{config.BOT_VERSION} | type /changelog for updates')

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
            description="**Subject:** 🎉 Celebrating 2k Servers!\n\n<:cleaner:954598059952734268> **Cleaner#8788** is reaching 2000 servers, keeping them clean and providing quality services. On September 3rd, 2022 we are going to have live stream on our Stage Channel in [Cleaner's Support Server](https://discord.gg/QrFEfNuC5m). Make sure to join us, I (Developer X) will be there to answer your questions and also we may play some games together 😉. So yeah stay tuned with us!\n\nRegards,\n*Developer X#0001*"
        )
        await database.execute(f"INSERT INTO NotificationView VALUES ({interaction.user.id}, 'viewed') ON CONFLICT (user_id) DO UPDATE SET status = 'viewed' WHERE user_id = {interaction.user.id}")
        await interaction.response.edit_message(content="<:done:954610357727543346> **Notification Viewed**", embed=embed, view=None)
        await database.commit()
        await database.close()

class Help(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @app_commands.command(name="help", description="Get a list of available commands")
    async def help(self, interaction: discord.Interaction):
        database = await aiosqlite.connect("data.db")
        await database.execute("CREATE TABLE IF NOT EXISTS NotificationView (user_id, status, PRIMARY KEY (user_id))")
        async with database.execute(f"SELECT status FROM NotificationView WHERE user_id = {interaction.user.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            resp_embed = discord.Embed(
                title="Where do you want to receive the help page?",
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
        Help(bot))