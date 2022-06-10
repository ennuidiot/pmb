import copy
import json
import logging
import os
import shutil
from datetime import datetime

import discord
import requests as r
from discord.ext import commands, tasks
from dotenv import load_dotenv


class Generic(commands.Cog):
    def _init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(
        name="sendtoconsole",
        brief="Sends a message to the bot console for Reece to read.",
        require_var_positional=True,
    )
    async def sendtoconsole(self, ctx, *, arg):
        await ctx.send("Thanks! Reece will see this... at some point...")
