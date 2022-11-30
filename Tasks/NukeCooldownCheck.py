import aiosqlite
import datetime
from discord.ext import commands, tasks

class NukeCooldownCheck(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.nuke_cooldown_check.start()

    @tasks.loop(seconds=1)
    async def nuke_cooldown_check(self):
        await self.bot.wait_until_ready()
        async with self.bot.database.execute(f"SELECT guild_id, timestamp FROM NukeCooldowns WHERE status = 'running'") as cursor:
            data = await cursor.fetchall()
        if data is None:
            return
        else:
            for entry in data:
                guild = self.bot.get_guild(entry[0])
                time = datetime.datetime.fromtimestamp(entry[1]).strftime("%Y-%m-%d")
                now_time = datetime.datetime.now().strftime("%Y-%m-%d")

                if now_time == time:
                    await self.bot.database.execute(f"DELETE FROM NukeCooldowns WHERE guild_id = {guild.id}")
                    await self.bot.database.commit()

async def setup(bot: commands.Bot):
    await bot.add_cog(
        NukeCooldownCheck(bot))