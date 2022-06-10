from datetime import datetime

import requests as r

import const


def get_guild(guild_id):
    return r.get(f"{const.API_URL}/guilds/{guild_id}")


def create_guild(id, name):
    return r.post(f"{const.API_URL}/guilds", json={"id": id, "name": name})


def update_guild(id, name, admin_role_id, admin_role_name):
    return r.patch(
        f"{const.API_URL}/guilds/{id}",
        json={
            "id": id,
            "name": name,
            "admin_role_id": admin_role_id,
            "admin_role_name": admin_role_name,
        },
    )

def create_watched_word(guild_id, watched_word_name):
    return r.post(
        f"{const.API_URL}/watched_words",
        json={
            "guild_id": guild_id,
            "name": watched_word_name,
            "last_mentioned": datetime.now().strftime(const.DATETIME_FORMAT),
        },
    )

def update_watched_word(guild_id, watched_word_name):
    return r.patch(
        f"{const.API_URL}/watched_words/{guild_id}/{watched_word_name}",
        json={
            "guild_id": guild_id,
            "name": watched_word_name,
            "last_mentioned": datetime.now().strftime(const.DATETIME_FORMAT),
        },
    )

def healthcheck():
    return r.post(f"{const.API_URL}/ht")