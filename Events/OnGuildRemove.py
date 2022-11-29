import aiosqlite
import discord
from discord import app_commands
from discord.ext import commands

class OnGuildRemove(commands.Cog):
    def _init_(self, bot: commands.Bot):
        self.bot = bot
    
    @commands.Cog.listener()
    async def on_guild_remove(self, guild: discord.Guild):
        auditDB = await aiosqlite.connect("./Databases/data.db")
        await auditDB.execute(f"DELETE FROM AuditChannels WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultAmount WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM BadwordFilter WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM DefaultPins WHERE guild_id = {guild.id}")
        await auditDB.execute(f"DELETE FROM DataTransfer WHERE guild_id = {guild.id}")
        await auditDB.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        OnGuildRemove(bot))