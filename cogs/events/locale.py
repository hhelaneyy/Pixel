import json
import disnake
import sqlite3
from disnake.ext import commands
import os

class Locale(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    async def get_user_locale(self, user_id):
        conn = sqlite3.connect('Pixel.db')
        c = conn.cursor()
        c.execute("SELECT language FROM locales WHERE user_id=?", (str(user_id),))
        result = c.fetchone()
        conn.close()
        return result[0].lower() if result else "en"

    async def get_translation(self, user_id, key):
        user_locale = await self.get_user_locale(user_id)
        filename = f"core/locale/{user_locale}.json"
        if not os.path.isfile(filename):
            filename = "core/locale/en.json"
        with open(filename, "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations.get(key, f"Translation missing for key: {key}")

    async def get_logs_locale(self, guild_id):
        conn = sqlite3.connect('Pixel.db')
        c = conn.cursor()
        c.execute("SELECT language FROM logs_locales WHERE guild_id=?", (str(guild_id),))
        result = c.fetchone()
        conn.close()
        return result[0].lower() if result else "en"

    async def get_logs_translation(self, guild_id, key):
        logs_locale = await self.get_logs_locale(guild_id)
        filename = f"core/locale/{logs_locale}.json"
        if not os.path.isfile(filename):
            filename = "core/locale/en.json"
        with open(filename, "r", encoding="utf-8") as file:
            translations = json.load(file)
        return translations.get(key, f"Translation missing for key: {key}")

def setup(bot: commands.Bot):
    bot.add_cog(Locale(bot))