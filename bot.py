import json
import logging
import os
from datetime import datetime

import discord
from discord.ext import commands, tasks
from dotenv import load_dotenv

import api
import const
from cogs import admin, generic, watched_words, weekdays

logging.getLogger().setLevel(logging.INFO)

intents = discord.Intents.default()
intents.message_content = True
intents.members = True

bot = commands.Bot(command_prefix="pmb!", intents=intents)

COGS = [weekdays.Weekdays, admin.Admin, generic.Generic, watched_words.WatchedWords]

# region Tasks

@tasks.loop(seconds=const.HEALTHCHECK_TIME_PERIOD)
async def healthcheck():
    healthcheck = api.healthcheck()
    if not healthcheck.ok:
        logging.error(f"Failed to send healthcheck - {healthcheck.reason}")

# endregion

# region Events

@bot.event
async def on_ready():
    logging.info("Loading cogs...")
    for cog in COGS:
        logging.info(f"Loading '{cog.__name__}'")
        await bot.add_cog(cog(bot))

    logging.info("Initializing...")

    for guild in bot.guilds:
        get_guild = api.get_guild(guild.id)
        if not get_guild.ok:
            if get_guild.status_code == 404:
                logging.info(f"No record of {guild.id}, creating...")
                make_guild = api.create_guild(guild.id, guild.name)
                if not make_guild.ok:
                    logging.error(
                        f"Failed to create record of {guild.id} - {make_guild.reason}"
                    )
                else:
                    logging.info(f"Successfully created record of guild {guild.id}")
            else:
                logging.info(
                    f"Request failed for guild {guild.id} - {get_guild.reason}"
                )

    healthcheck.start()

    logging.info("Done initializing!")


@bot.event
async def on_guild_join(guild):
    logging.info(f"bot joined guild {guild}, system channel is {guild.system_channel}")


# @bot.event
# async def on_message(message):
#     if message.author == bot.user:
#         return
    
#     if message.content.endswith("...2!") or message.content.endswith("...two!"):
#         await message.channel.send(file=discord.File('./images/peggle.gif'))

#     await bot.process_commands(message)


# endregion

if __name__ == "__main__":
    try:
        bot.run(const.TOKEN)
    finally:
        logging.info("Goodbye!")
