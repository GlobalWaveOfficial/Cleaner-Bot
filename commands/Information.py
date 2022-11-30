import discord
import datetime, time
from discord import app_commands
from discord.ext import commands
import config

startTime = time.time()

class Information(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot
        
    @app_commands.command(name="info", description="Show's information about the bot")
    async def info(self, interaction: discord.Interaction):
        botinfo = await self.bot.application_info()
        count = 0
        for guild in self.bot.guilds:
            count += guild.member_count

        info_embed = discord.Embed(
            title="Cleaner#8788",
            description="**An Advanced Cleaning Utility**",
            color=discord.Color.magenta()
        )
        info_embed.set_thumbnail(url="https://i.imgur.com/T12D7JH.png")
        info_embed.add_field(name="Founder of Cleaner", value=botinfo.owner, inline=True)
        info_embed.add_field(name="Developers", value=f"{botinfo.owner}\nsarth#0460", inline=True)
        info_embed.add_field(name="Beta Testers", value=f"RVG|𝓵𝓸𝓻𝔂#9995\nGod Of Life#2140\nTomClancy#0575", inline=True)
        info_embed.add_field(name="Graphics by", value="Freepik at FlatIcon:\nhttps://www.flaticon.com/authors/freepik", inline=False)
        info_embed.add_field(name="Development Language", value="Python", inline=True)
        info_embed.add_field(name="Host", value="Oracle Cloud VPS", inline=True)
        info_embed.add_field(name="Uptime", value=str(datetime.timedelta(seconds=int(round(time.time()-startTime)))), inline=True)
        info_embed.add_field(name="Ping", value=f"{round(self.bot.latency * 1000)} ms", inline=True)
        info_embed.add_field(name="Language", value="EN-US", inline=True)
        info_embed.add_field(name="Version", value=f"v{config.BOT_VERSION}", inline=True)
        info_embed.add_field(name="Guild Count", value=len(self.bot.guilds), inline=True)
        info_embed.add_field(name="Member Count", value=count, inline=True)
        info_embed.add_field(name="Command Count", value=25, inline=True)
        info_embed.add_field(name="Bot Invite", value="http://dsc.gg/ccleaner", inline=True)
        info_embed.add_field(name="Support Server", value="https://dsc.gg/cleaner-support", inline=True)
        info_embed.set_footer(text="Chech out latest updates! do /changelog")

        await interaction.response.send_message(embed=info_embed, ephemeral=True)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Information(bot))

#self.bot.application_info()