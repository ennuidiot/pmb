import json
import logging
import string
import sys
from datetime import datetime

from discord.ext import commands

import api
import const


class WatchedWords(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    async def _handle_watched_word_mention(self, message, watched_word):
        # remove all characters that could signify the end of a word
        cleaned_message_content = message.content.lower().translate(
            str.maketrans("", "", string.punctuation)
        )
        if watched_word["name"].lower() in cleaned_message_content.split(" "):
            update_watched_word = api.update_watched_word(
                message.guild.id, watched_word["name"]
            )
            if watched_word["last_mentioned"] is not None:
                days_since_last = datetime.now() - datetime.strptime(
                    watched_word["last_mentioned"], const.DATETIME_FORMAT
                )

                if days_since_last.days == 0:
                    content = f"'{watched_word['name'].title()}'? Again? It hasn't even been a day yet!"
                else:
                    content = f"You fuckers made it {days_since_last.days} day{'s' if days_since_last.days != 1 else ''} without saying '{watched_word['name']}'."
            else:
                content = f"They told me this would happen. Someone's mentioned '{watched_word['name']}'."

            watched_word_info_string = f"watched word '{watched_word['name']}' for guild '{message.guild.name}' ({message.guild.id})"

            if not update_watched_word.ok:
                content = f"{content} Luckily for you, I'm going to ignore this one."
                logging.error(
                    f"Failed to update {watched_word_info_string} - {update_watched_word.content.decode(sys.stdout.encoding)}"
                )
            else:
                content = f"{content} Resetting the counter." if watched_word["last_mentioned"] is not None else f"{content} I'll remember this."
                logging.info(f"Successfully updated {watched_word_info_string}")
            await message.channel.send(content)


    @commands.Cog.listener("on_message")
    async def handle_watched_words(self, message):
        if message.author == self.bot.user:
            return

        ctx = await self.bot.get_context(message)
        if ctx.valid and ctx.command is not None:
            # ignore message for watched words if it's a valid command
            return
        get_watched_words = api.get_guild(message.guild.id)
        if not get_watched_words.ok:
            logging.error(
                f"Couldn't get watched_words for '{message.guild.name}' ({message.guild.id}) - {get_watched_words.status_code}"
            )
        else:
            watched_words = json.loads(get_watched_words.content.decode("utf-8"))[
                "watched_words"
            ]
            for watched_word in watched_words:
                await self._handle_watched_word_mention(message, watched_word)