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


class Weekdays(commands.Cog):
    def _init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="monday")
    async def monday(self, ctx):
        await ctx.send(
            "Hey guess what I'm having today? Fuck man, fuckin' steak baby yeah! The rib eye, mashed potatoes, beans. Yeah baby, fuck. Fuckin' steak, yeah. Monday brunch baby, fuck. This is what to make on your Monday, fuck. Any day, is wh... What makes it your day make it a happy one. Fuck man, fuck. Fuckin' steak baby yeah, it's fuckin' Monday.\n\nYeah fuckin' Monday baby, fucking Monday. Steak baby, fucking Monday. Fuck. All right, make Monday a good day baby, yeah."
        )

    @commands.command(name="tuesday")
    async def tuesday(self, ctx):
        await ctx.send(
            "https://images-ext-2.discordapp.net/external/N7XBaprPKIDej3KlOJ9omGyT_gmqmyMWQ_wG2cXROF8/https/pics.me.me/thumb_joshpeck-chickensnack-tuesday-again-no-problem-i-think-we-need-tuesday-71456531.png"
        )

    @commands.command(name="wednesday")
    async def wednesday(self, ctx):
        await ctx.send(
            "yeah fried chicken wednesday baby yeah fuckin it's one of my favorite nights because of fried chicken yeah fuckin wednesday night baby fuckin fried chicken yep fried chicken wednesday fried chicken wednesday who deserves fried chicken me I deserve fried chicken it's fuckin wednesday wednesday night fried chicken yeah closer to the weekend thursday the-and then friday here comes the weekend here comes the weekend fuckin fuckin wednesday night fried chicken wednesday baby who deserves fried chicken me who deserves fried chicken me love fried chicken chicken wednesday baby fuckin fried chicken wednesday wednesday night baby fried chicken wednesday yeah"
        )

    @commands.command(name="thursday")
    async def thursday(self, ctx):
        await ctx.send("https://youtu.be/d7xMgJedN2s")

    @commands.command(name="friday")
    async def sunday(self, ctx):
        await ctx.send(
            "happy electric feel friday\nhttps://va.media.tumblr.com/tumblr_qk677t530F1z1wx4n_720.mp4"
        )

    @commands.command(name="saturday")
    async def saturday(self, ctx):
        await ctx.send("https://youtu.be/Xud0YWhQsXc")

    @commands.command(name="sunday")
    async def sunday(self, ctx):
        await ctx.send(
            "https://images-ext-1.discordapp.net/external/QDNhdwAIh2-OVD3kOxFwrSWUaFM21sBfSfLeYyP6HO8/https/i.kym-cdn.com/entries/icons/original/000/026/806/Screen_Shot_2018-07-30_at_2.39.51_PM.jpg?width=960&height=572"
        )