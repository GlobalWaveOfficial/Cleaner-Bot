import asyncio
import os
import discord
from discord import app_commands
from discord.ext import commands
from discord.ext import tasks
import config
import topgg

intents = discord.Intents.default()
intents.message_content = True

class MyBot(commands.Bot):
    def __init__(self):
        super().__init__(
            command_prefix=config.PREFIX,
            intents= intents,
            status=discord.Status.idle,
            activity=discord.Game(name="working on v6.2"),
            application_id = config.APPLICATION_ID
        )

    async def setup_hook(self):
        for filename in os.listdir("./commands"):
            if filename.endswith('.py'):
                await self.load_extension(f"commands.{filename[:-3]}")
                print(f"Loaded {filename}")
            
            if filename.startswith('__'):
                pass
        await bot.tree.sync()

bot = MyBot()

@bot.event
async def on_ready():
    print(f"{bot.user} is connected to Discord, current latency is {round(bot.latency * 1000)}ms")

@bot.command(name="reload")
@commands.is_owner()
async def reload(ctx: commands.Context, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.reload_extension(f"cogs.{cog}")
    await ctx.send(f"🔁 {cog} reloaded!")

@bot.command(name="load")
@commands.is_owner()
async def load(ctx: commands.Context, cog:str):
    # Reloads the file, thus updating the Cog class.
    await bot.load_extension(f"cogs.{cog}")
    await ctx.send(f"🆙 {cog} loaded!")

@bot.command()
async def membercount(ctx):
    count = 0
    for guild in bot.guilds:
        count += guild.member_count
    
    await ctx.send(count)

bot.run(config.BOT_TOKEN)
