import aiosqlite
import datetime
import discord
from discord import app_commands
from discord.ext import commands

class OnMessage(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        try:
            async with auditDB.execute(f"SELECT words FROM BadwordFilter WHERE guild_id = {message.channel.guild.id}") as cursor1:
                data = await cursor1.fetchone()
            if data is None:
                pass
            else:
                try:
                    words = data[0].split(",")
                    for word in words:
                        if word in message.content:
                            await message.delete()
                except:
                    word = data[0]
                    if word in message.content:
                        await message.delete()
        except:
            pass

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnMessage(bot))