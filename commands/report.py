import traceback
import discord
import aiosqlite
from discord.ui import Modal, View, button, Button
from discord import app_commands, ButtonStyle
from discord.ext import commands

class ReplyModal(Modal, title="Report/Suggestion Reply"):
    def __init__(self):
        super().__init__(timeout=None)
    
    reply = discord.ui.TextInput(
        label="Your reply",
        style=discord.TextStyle.long,
        placeholder="Type your reply here...",
        required=True
    )

    async def on_submit(self, interaction: discord.Interaction):
        async with auditDB.execute(f"SELECT user_id, title, content, upvotes, downvotes FROM ReportsAndSuggestions WHERE message_id = {interaction.message.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            await interaction.response.send_message("<:error:954610357761105980> Oops! Something went wrong...", ephemeral=True)
        else:
            user = await interaction.client.fetch_user(data[0])
            try:
                await user.send(content=f"<:notif:1013118962873147432> **You have a new reply on your report/suggestion post!**\n\n**{interaction.user.name}** has replied to your following post:\n\n> **{data[1]}**\n> {data[2]}\n\n**Votes:** <:upvote:1026912667824312350> `{data[3]}` <:downvote:1026912669812412437> `{data[4]}`\n\n**Reply:** {self.reply}")
                await interaction.response.send_message("<:mailsent:1026906494257594419> Your message has been delivered.", ephemeral=True)
            except discord.errors.Forbidden:
                await interaction.response.send_message(f"<:error:954610357761105980> I'm unable to DM {user.name}, instead I've sent the message to their mailbox.", ephemeral=True)

class ReportButtons(View):
    def __init__(self):
        super().__init__(timeout=None)
    
    @button(label="Reply", style=ButtonStyle.green, custom_id="reply_button")
    async def reply_func(self, interaction: discord.Interaction, button: Button):
        role = interaction.guild.get_role(1004052000415162398)
        if role in interaction.user.roles:
            await interaction.response.send_modal(ReplyModal())
        else:
            await interaction.response.send_message(content="<:error:954610357761105980> Hey!! You can't do that!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji="<:upvote:1026912667824312350>", custom_id="upvote_button")
    async def upvote_button(self, interaction: discord.Interaction, button: Button):
        await auditDB.execute(f"UPDATE ReportsAndSuggestions SET upvotes = upvotes + 1 WHERE message_id = {interaction.message.id}")
        await auditDB.commit()
        await interaction.response.send_message(content="<:done:954610357727543346> Success!", ephemeral=True)
    
    @button(style=ButtonStyle.gray, emoji="<:downvote:1026912669812412437>", custom_id="downvote_button")
    async def downvote_button(self, interaction: discord.Interaction, button: Button):
        await auditDB.execute(f"UPDATE ReportsAndSuggestions SET downvotes = downvotes + 1 WHERE message_id = {interaction.message.id}")
        await auditDB.commit()
        await interaction.response.send_message(content="<:done:954610357727543346> Success!", ephemeral=True)

class BugReport(discord.ui.Modal, title="Report"):
    heading = discord.ui.TextInput(
        label="Title of your report",
        style=discord.TextStyle.short,
        placeholder="Type the title of your report, i.e Commands not working",
        required=True,
        max_length=30
    )

    report = discord.ui.TextInput(
        label="Tell us what you want to report",
        style=discord.TextStyle.long,
        placeholder="Describe your issue in detail",
        required=True,
        max_length=1000
    )

    async def on_submit(self, interaction: discord.Interaction):
        channel = interaction.client.get_channel(1004064457204437152)
        suggestion_embed = discord.Embed(
            title=self.heading,
            description=self.report,
            color=discord.Color.magenta()
        )
        suggestion_embed.set_author(name=interaction.user, icon_url=interaction.user.avatar)
        msg = await channel.send(embed=suggestion_embed, view=ReportButtons())
        await auditDB.execute(f'INSERT INTO ReportsAndSuggestions VALUES ({interaction.guild.id}, {interaction.user.id}, {msg.id}, "{self.heading}", "{self.report}", 0, 0)')
        await interaction.response.send_message("<:thankyou:966151700018765835> Your report has been sent!", ephemeral=True)
        await auditDB.commit()
        return

    async def on_error(self, interaction: discord.Interaction, error: Exception):
        await interaction.response.send_message("<:error:954610357761105980> Oops! Something went wrong.", ephemeral=True)

        traceback.print_tb(error.__traceback__)

class Report(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        global auditDB
        auditDB = await aiosqlite.connect("data.db")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS AuditChannels (guild_id, channel_id, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS DefaultAmount (guild_id, default_amount, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS BadwordFilter (guild_id, words, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS DefaultPins (guild_id, condition, PRIMARY KEY (guild_id))")
        await auditDB.execute("CREATE TABLE IF NOT EXISTS ReportsAndSuggestions (guild_id, user_id, message_id, title, content, upvotes, downvotes, PRIMARY KEY (message_id))")

    @app_commands.command(name="report", description="Experiencing Issues? Report it to us!")
    async def report(self, interaction: discord.Interaction):
        await interaction.response.send_modal(BugReport())

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Report(bot))