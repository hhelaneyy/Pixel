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
        channel = await self.bot.fetch_channel(1228412432599482389)

        if blacklisted:
            cursor.execute('INSERT OR REPLACE INTO blacklist VALUES (?, ?)', (user.id, blacklisted))
            conn.commit()

            if user.id == self.bot.owner.id or user.id == self.bot.user.id:
                await inter.response.send_message('⚠️ Этих пользователей нельзя занести в ЧС вечеринки..)', ephemeral=True)
                return
            else:
                await inter.response.send_message('✅', ephemeral=True)

                E = disnake.Embed(color=0xff0000)
                E.add_field(name='Нарушитель:', value=user.mention)
                E.add_field(name='Действие:', value=f'```Положение статуса ЧС изменено на: {blacklisted}.```')
                E.add_field(name='Причина:', value='```Нарушение политики использования Pixel.```', inline=False)
                E.set_author(name=inter.author.name, icon_url=inter.author.avatar)
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await channel.send(embed=E)

        else:
            cursor.execute('DELETE FROM blacklist WHERE user_id = ?', (user.id,))
            conn.commit()

            await inter.response.send_message('✅', ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(OwnerCog(bot))