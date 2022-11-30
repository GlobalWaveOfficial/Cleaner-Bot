import aiosqlite
import datetime
import discord
from discord import app_commands
from discord.ext import commands

class OnMessageEdit(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message_edit(self, before: discord.Message, after: discord.Message):
        if before.author.bot:
            return
        if before.content == after.content:
            return
        Time = datetime.datetime.now()
        UpTime = Time.strftime("%d-%m-%Y %H:%M:%S")

        async with self.bot.database.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {before.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            channel = self.bot.get_channel(data[0])
            await channel.send(embed= discord.Embed(title="Message Edited!", description= f"<:time:954610357576548444> **Time** `{UpTime}`\n<:author:954610357761081424> **Author** {before.author.mention}\n<:channel:954457643227942923> **Channel** {before.channel.mention}\n<:messages:954610357773684837> **Messages**\n**Original Message:** {before.content}\n**Edited Message:** {after.content}", color=discord.Color.magenta()))

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessageEdit(bot))