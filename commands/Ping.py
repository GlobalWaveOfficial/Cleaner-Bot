import discord
from discord import app_commands
from discord.ext import commands

class Ping(commands.Cog):
    def __init__(self, bot: commands.Bot) -> None:
        self.bot = bot

    @app_commands.command(name="ping", description="Show's bot latency")
    async def ping(self, interaction: discord.Interaction):
        await interaction.response.defer(ephemeral=True)
        latency = round(self.bot.latency * 1000)

        if latency < 150:
            if latency < 75:
                await interaction.followup.send(f"<:latency:954610357647851550> **Bot Latency:** <:signal5:954624490132873256> `{latency}`ms", ephemeral=True)
                return
            else:
                await interaction.followup.send(f"<:latency:954610357647851550> **Bot Latency:** <:signal4:954624489570844692>`{latency}`ms", ephemeral=True)
                return

        if latency > 150:
            if latency > 300:
                await interaction.followup.send(f"<:latency:954610357647851550> **Bot Latency:** <:signal1:954624489197559828>`{latency}`ms", ephemeral=True)
                return
            if latency > 225:
                await interaction.followup.send(f"<:latency:954610357647851550> **Bot Latency:** <:signal2:954624489340153906>`{latency}`ms", ephemeral=True)
                return
            else:
                await interaction.followup.send(f"<:latency:954610357647851550> **Bot Latency:** <:signal3:954624491558936596>`{latency}`ms", ephemeral=True)
                return

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(
        Ping(bot))