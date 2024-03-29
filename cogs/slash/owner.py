from datetime import datetime
import os
import random 
from core.utilities.embeds import footer
import sqlite3
import disnake
from disnake.ext import commands

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS blacklist (
               user_id INTEGER PRIMARY KEY,
               blacklisted INTEGER
               )
               ''')
conn.commit()

class OwnerCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Организатор дал мне право наказывать нарушителей. <3', guild_ids=[1211231259607564298])
    async def owner(self, inter):
        ...

    @owner.sub_command(name='blacklist', description='У нас завёлся плохой мальчик?')
    @commands.is_owner()
    async def blacklist(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, blacklisted: bool = commands.Param(choices=[True, False])):
        if blacklisted:
            cursor.execute('INSERT OR REPLACE INTO blacklist VALUES (?, ?)', (user.id, blacklisted))
            conn.commit()

            if user.id == self.bot.owner.id or user.id == 585427658775461909 or user.id == self.bot.user.id:
                await inter.response.send_message('⚠️ Этих пользователей нельзя занести в ЧС вечеринки..)', ephemeral=True)
                return
            else:
                await inter.response.send_message('✅', ephemeral=True)

        else:
            cursor.execute('DELETE FROM blacklist WHERE user_id = ?', (user.id,))
            conn.commit()

            await inter.response.send_message('✅', ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(OwnerCog(bot))