import discord
import config

changelog_embed = discord.Embed(
    colour=discord.Color.magenta()
)

changelog_embed.set_author(name='Last Updated on November 29, 2022', icon_url='https://i.imgur.com/T12D7JH.png')
changelog_embed.set_thumbnail(url='https://i.imgur.com/T12D7JH.png')
changelog_embed.add_field(name="Message Cleaning using Words or Phrases", value="Message cleaning will support deleting only those messages which contains a specific word or phrase.", inline=False)
changelog_embed.add_field(name="Default Values will apply on other cleaning commands", value="The default value specified for message deletion will apply to other clean commands.", inline=False)
changelog_embed.add_field(name="Across Server Deletion", value="Ability to delete someone's messages across an entire server, not just in one channel.", inline=False)
changelog_embed.add_field(name="Stay Updated", value="Now you can receive latest messages by us, the notification will be shown under `/help` and `/changelog` commands.", inline=False)
changelog_embed.set_footer(text=f'v{config.BOT_VERSION} | type /report to send bug reports to us')