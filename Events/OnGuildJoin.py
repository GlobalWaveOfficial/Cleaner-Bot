import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class OnGuildJoin(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT channel_id FROM AuditChannels WHERE guild_id = {channel.guild.id}") as cursor:
            data = await cursor.fetchone()
        if data is None:
            pass
        else:
            if channel.id == data[0]:
                await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {channel.guild.id}")
                await auditDB.commit()
            else:
                pass

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnGuildJoin(bot))