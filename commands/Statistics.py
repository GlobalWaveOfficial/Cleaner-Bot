from discord.ext import commands, tasks

class Statistics(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.update_stats.start()
    
    @tasks.loop(minutes=15)
    async def update_stats(self):
        await self.bot.wait_until_ready()
        total_count = 0
        for guild in self.bot.guilds:
            total_count += guild.member_count

        count = f'{total_count}'

        if len(count) >= 3:
            count = count

        if 3 < len(count) <= 6:
            count = f"{count[:-3]}k"

        if 7 <= len(count) <= 9:
            count = f"{count[:-6]}m"

        cleaner_latency = self.bot.get_channel(1004329804318908436)
        server_count = self.bot.get_channel(1004330060448284692)
        shard_count = self.bot.get_channel(1026930650206449665)
        member_count = self.bot.get_channel(1004338709019230341)

        await cleaner_latency.edit(name=f"Cleaner Latency: {round(self.bot.latency * 1000)}ms")
        await server_count.edit(name=f"Server Count: {len(self.bot.guilds)}")
        await shard_count.edit(name=f"Shard Count: {self.bot.shard_count}")
        await member_count.edit(name=f"Member Count: {count}")

async def setup(bot: commands.Bot):
    await bot.add_cog(Statistics(bot))