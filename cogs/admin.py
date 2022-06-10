import json
import logging
import sys
from datetime import datetime, timedelta

import discord
import pandas as pd
from discord.ext import commands, tasks

import api
import const


def guild_owner_only():
    async def predicate(ctx):
        return ctx.author == ctx.guild.owner

    return commands.check(predicate)


def admin_role_only():
    async def predicate(ctx):
        get_guild = api.get_guild(ctx.guild.id)
        if not get_guild.ok:
            logging.error(f"Failed to get admin role id of guild '{ctx.guild.name}' ({ctx.guild.id}) for admin_role_only predicate")
            return False
        return json.loads(get_guild.content.decode('utf-8'))['admin_role_id'] in [
            role.id for role in ctx.author.roles
        ]

    return commands.check(predicate)

def guild_data_to_nice_dict(guild_data):
    now = datetime.now()
    def watched_word_data_to_nice_string(watched_word_data):
        days_since = (now - datetime.strptime(watched_word_data["last_mentioned"], const.DATETIME_FORMAT)).days
        days_since_str = f"{days_since} day{'s' if days_since > 1 else ''} ago" if days_since != 0 else "in the last day"
        return f"`{watched_word_data['name']}`, mentioned {days_since_str}"

    return {
        "ID": guild_data["id"],
        "Admin Role": f"<@&{guild_data['admin_role_id']}>",
        # "Watched Words": [{'Word': word['name'], 'Last Mentioned': word['last_mentioned']} for word in guild_data['watched_words']]
        "Watched Words": "\n".join(watched_word_data_to_nice_string(word) for word in guild_data["watched_words"])
    }

class Admin(commands.Cog):
    def _init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.command(name="setadminrole")
    @guild_owner_only()
    async def setadminrole(self, ctx, arg):
        for role in ctx.guild.roles:
            if role.mention == arg:
                update_guild = api.update_guild(ctx.guild.id, ctx.guild.name, role.id, role.name)
                if not update_guild.ok:
                    logging.error(
                        f"Couldn't set {ctx.guild.name} ({ctx.guild.id}) admin_role_id to '{arg}' - {update_guild.content}"
                    )
                    await ctx.send(f"Couldn't set {arg} as an admin role. Ask the dev why.")
                    return
                logging.info(
                    f"Set {ctx.guild.name} ({ctx.guild.id}) admin_role_id to '{arg}'"
                )
                await ctx.send(f"Admin role set to {role.mention}.")


    @commands.command(name="addwatchedword")
    @admin_role_only()
    async def add_watched_word(self, ctx, arg):
        add_watched_word = api.create_watched_word(ctx.guild.id, arg)
        watched_word_info_string = f"watched word '{arg}' for guild '{ctx.guild.name}' ({ctx.guild.id})"
        if add_watched_word.ok:
            logging.info(f"Successfully added {watched_word_info_string}.")
            await ctx.send(f"Added '{arg}' to list of watched words.")
        else:
            logging.error(f"Failed to add {watched_word_info_string} - {add_watched_word.content.decode(sys.stdout.encoding)}")
            await ctx.send(f"Failed to add '{arg}' to list of watched words.")


    @commands.command(name="getguilddata")
    @admin_role_only()
    async def get_guild_data(self, ctx):
        get_guild_data = api.get_guild(ctx.guild.id)
        if not get_guild_data.ok:
            await ctx.send("Couldn't get guild data.")
            return
        guild_data = guild_data_to_nice_dict(json.loads(get_guild_data.content.decode("utf-8")))
        embed = discord.Embed(
            title=f"Data for '{ctx.guild.name}'",
        )
        for key in guild_data:
            embed.add_field(name=key, value=guild_data[key], inline=False)
        await ctx.send(embed=embed)

    async def last_x_days_activity(self, guild, days=None):
        logging.info(f"Generating activity report for guild '{guild.name}' ({guild.id})")
        # TODO: activity report
        messages = []
        messages_count = 0
        after = None if days is None else (datetime.now() - timedelta(days=days))
        for channel in guild.channels:
            if isinstance(channel, discord.TextChannel):
                async for msg in channel.history(after=after, limit=None):
                    if not msg.author.bot:
                        messages.append({'id': msg.id, 'channel': msg.channel, 'author': msg.author})
                        messages_count += 1
                        print(messages_count)
        
        df = pd.DataFrame.from_dict(messages)
        embed = discord.Embed(title=f"Activity since {after or 'the beginning of time'}")
        embed.add_field(name="Total messages", value=df.count()['id'], inline=True)
        top_five_channels_list = "\n".join(f"{i}. {channel}: {count}" for i, (channel, count) in enumerate(df['channel'].value_counts().head(5).to_dict().items()))
        top_five_authors_list = "\n".join(f"{i}. {author}: {count}" for i, (author, count) in enumerate(df['author'].value_counts().head(5).to_dict().items()))
        embed.add_field(name="Top 5 Most Active Channels", value=top_five_channels_list, inline=False)
        embed.add_field(name="Top 5 Most Active Users", value=top_five_authors_list, inline=False)

        return embed

    @commands.command(name="dailyactivityreport")
    @admin_role_only()
    async def daily_activity_report(self, ctx):
        return await ctx.send(embed=await self.last_x_days_activity(ctx.guild, days=1))

    @commands.command(name="weeklyactivityreport")
    @admin_role_only()
    async def weekly_activity_report(self, ctx):
        return await ctx.send(embed=await self.last_x_days_activity(ctx.guild, days=7))

    @commands.command(name="overallactivityreport")
    @admin_role_only()
    async def overall_activity_report(self, ctx):
        return await ctx.send(embed=await self.last_x_days_activity(ctx.guild))


    # @tasks.loop(time=datetime.time(hour=0, minute=0, tzinfo=datetime.timezone.utc))
    # async def server_report(self):
    #     activity = await self.last_days_activity()