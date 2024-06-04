import json
import disnake
import sqlite3
import os
import asyncio
from disnake.ext import commands
from concurrent.futures import ThreadPoolExecutor

class Locale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.executor = ThreadPoolExecutor()

    async def fetch_one(self, query, params):
        def db_query(query, params):
            conn = sqlite3.connect('Pixel.db')
            c = conn.cursor()
            c.execute(query, params)
            result = c.fetchone()
            conn.close()
            return result

        loop = asyncio.get_event_loop()
        return await loop.run_in_executor(self.executor, db_query, query, params)

    async def get_user_locale(self, user_id):
        query = "SELECT language FROM locales WHERE user_id=?"
        result = await self.fetch_one(query, (str(user_id),))
        return result[0].lower() if result else "en"

    async def get_translation(self, user_id, key):
        user_locale = await self.get_user_locale(user_id)
        filename = f"core/locale/{user_locale}.json"
        if not os.path.isfile(filename):
            filename = "core/locale/en.json"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations.get(key, f"Translation missing for key: {key}")
        except (FileNotFoundError, json.JSONDecodeError):
            return f"Error loading translations for locale: {user_locale}"

    async def get_logs_locale(self, guild_id):
        query = "SELECT language FROM logs_locales WHERE guild_id=?"
        result = await self.fetch_one(query, (str(guild_id),))
        return result[0].lower() if result else "en"

    async def get_logs_translation(self, guild_id, key):
        logs_locale = await self.get_logs_locale(guild_id)
        filename = f"core/locale/{logs_locale}.json"
        if not os.path.isfile(filename):
            filename = "core/locale/en.json"
        try:
            with open(filename, "r", encoding="utf-8") as file:
                translations = json.load(file)
            return translations.get(key, f"Translation missing for key: {key}")
        except (FileNotFoundError, json.JSONDecodeError):
            return f"Error loading translations for locale: {logs_locale}"

def setup(bot: commands.Bot):
    bot.add_cog(Locale(bot))