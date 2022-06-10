import os

from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")

API_URL = os.getenv("API_URL")

DATETIME_FORMAT = "%Y-%m-%dT%H:%M:%S.%f"

HEALTHCHECK_TIME_PERIOD = 10
