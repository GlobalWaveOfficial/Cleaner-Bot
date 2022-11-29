import discord
import config

help_embed = discord.Embed(
    colour=discord.Color.magenta()
)

help_embed.set_author(name='Cleaner Bot Commands',icon_url='https://i.imgur.com/T12D7JH.png')
help_embed.set_thumbnail(url='https://i.imgur.com/T12D7JH.png')
help_embed.add_field(name='Help', value='Shows this message', inline=False)
help_embed.add_field(name="**__Cleaning Commands:__**", value="These commands can be found under /clean command group\n**Clean:** Delete a specified number of messages.\n**User:** Delete a specified of messages sent by the mentioned user.\n**Bot:** Delete a specified number of messages sent by bots.\n**Mass Delete:** Delete someone's messages all across the server, instead of one current channel.", inline=False)
help_embed.add_field(name="**__Delete Commands:__**", value="These commands can be found under /delete command group\n**Channel:** Delete the mentioned channel.\n**Category:** Delete the mentioned category.\n**Role:** Delete the mentioned role.\n**Thread:** Delete the mentioned thread.\n**Emoji:** Delete the specified emoji.\n**Nickname:** Delete the nickname of the mentioned user set in current server.", inline=False)
help_embed.add_field(name="**__Purge Commands:__**", value="These commands can be found under /purge command group\n**Channel:** Deletes and re-creates the mentioned or current channel, with same permissions.\n**Category:** Deletes and re-creates the current category", inline=False)
help_embed.add_field(name="**__Settings Commands:__**", value="These commands can be found under /settings command group\n**Audit Channel:** Set a channel to get message logs.\n**Auto Delete:** Set automatic message deletion in a specific channel and after certain time, the channel will be recreated.\n**Default Pin Condition:** Set default pin check condition, it'll be check when using `/clean messages` command.\n**Default Amount:** Set default cleaning amount for clean message command\n**Reset:** Reset all settings for the current server.\n**Show:** View the current settings for the server.", inline=False)
help_embed.add_field(name="**__Special Commands:__**", value="Following command can be invoked by server owner only.\n**Nuke:** Wipes everything from the server except members, THIS IS A DANGEROUS COMMAND!", inline=False)
help_embed.add_field(name="**__Help & Support:__**", value="**Report:** Facing issues using the bot? submit the report by /report\n**Suggestion:** Want something to get added to bot? Tell us your ideas /suggestion", inline=False)
help_embed.add_field(name="**__Other Commands:__**", value="**Permissions Check:** Check if the bot has all necessary permisions to work properly\n**Info** Show bot's information\n**Changelog:** Show latest changelog.\n**Ping:** Show bot's current latency.\n**Help:** Shows this message.", inline=False)
help_embed.set_footer(text=f'v{config.BOT_VERSION} | type /changelog for updates')