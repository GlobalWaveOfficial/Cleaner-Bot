import aiosqlite
from discord.ext import commands, tasks

class AutoDeleteTasks(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.auto_delete_60.start()
        self.auto_delete_180.start()
        self.auto_delete_300.start()
    
    @tasks.loop(minutes=1)
    async def auto_delete_60(self):
        await self.bot.wait_until_ready()
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT guild_id, channel_1 FROM AutoDeleteChannels WHERE duration_1 = 60") as cursor:
            data = await cursor.fetchall()
        if data is None:
            return
        else:
            for entry in data:
                guild = self.bot.get_guild(entry[0])
                channel = guild.get_channel(entry[1])

                pos = channel.position
                cat = channel.category
                await channel.delete(reason="Auto-delete channel purge (deleteing channel)")
                chnl = await channel.clone(reason="Auto-delete channel purge (cloning channel)")
                await chnl.edit(category=cat, position=pos, reason="Auto-delete channel purge (adjusting position)")
                await auditDB.execute(f"UPDATE AutoDeleteChannels SET channel_1 = {chnl.id} WHERE guild_id = {entry[0]}")
                await auditDB.commit()
    
    @tasks.loop(minutes=3)
    async def auto_delete_180(self):
        await self.bot.wait_until_ready()
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT guild_id, channel_1 FROM AutoDeleteChannels WHERE duration_1 = 180") as cursor:
            data = await cursor.fetchall()
        if data is None:
            return
        else:
            for entry in data:
                guild = self.bot.get_guild(entry[0])
                channel = guild.get_channel(entry[1])

                pos = channel.position
                cat = channel.category
                await channel.delete(reason="Auto-delete channel purge (deleteing channel)")
                chnl = await channel.clone(reason="Auto-delete channel purge (cloning channel)")
                await chnl.edit(category=cat, position=pos, reason="Auto-delete channel purge (adjusting position)")
                await auditDB.execute(f"UPDATE AutoDeleteChannels SET channel_1 = {chnl.id} WHERE guild_id = {entry[0]}")
                await auditDB.commit()
    
    @tasks.loop(minutes=5)
    async def auto_delete_300(self):
        await self.bot.wait_until_ready()
        auditDB = await aiosqlite.connect("./Databases/data.db")
        async with auditDB.execute(f"SELECT guild_id, channel_1 FROM AutoDeleteChannels WHERE duration_1 = 300") as cursor:
            data = await cursor.fetchall()
        if data is None:
            return
        else:
            for entry in data:
                guild = self.bot.get_guild(entry[0])
                channel = guild.get_channel(entry[1])

                pos = channel.position
                cat = channel.category
                await channel.delete(reason="Auto-delete channel purge (deleteing channel)")
                chnl = await channel.clone(reason="Auto-delete channel purge (cloning channel)")
                await chnl.edit(category=cat, position=pos, reason="Auto-delete channel purge (adjusting position)")
                await auditDB.execute(f"UPDATE AutoDeleteChannels SET channel_1 = {chnl.id} WHERE guild_id = {entry[0]}")
                await auditDB.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        AutoDeleteTasks(bot))
