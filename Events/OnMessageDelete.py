import aiosqlite
import datetime
import discord
from discord import app_commands
from discord.ext import commands

class OnMessageDelete(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message_delete(self, message: discord.Message):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        if message.author.bot:
            return
        Time = datetime.datetime.now()
        UpTime = Time.strftime("%d-%m-%Y %H:%M:%S")

        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {message.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            channel = message.guild.get_channel(data[0])
            await channel.send(embed= discord.Embed(title="Message Deleted!", description= f"<:time:954610357576548444> **Time** `{UpTime}`\n<:author:954610357761081424> **Author** {message.author.mention}\n<:channel:954457643227942923> **Channel** {message.channel.mention}\n<:messages:954610357773684837> **Message Content:** {message.content}", color=discord.Color.magenta()))

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessageDelete(bot))