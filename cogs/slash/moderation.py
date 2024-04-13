import random
import disnake
from disnake.ext import commands
import sqlite3
from core.utilities.embeds import footer

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS warns (
            guild_name TEXT,
            user_id TEXT,
            w_count INTEGER
        )
''')
conn.commit()

class ModCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Организатор дал мне право наказывать нарушителей. <3')
    async def moderation(self, inter):
        ...

    @moderation.sub_command(name='ban', description='Организатор вечеринки разрешил мне банить плохишей <3')
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, reason):
        guild = inter.guild

        await guild.ban(user, reason)
        E = disnake.Embed(title='🛑 Нарушитель был забанен', color=0xff0000)
        E.add_field(name='Администратор:', value=inter.author.mention)
        E.add_field(name='Нарушитель:', value=user.mention)
        E.add_field(name='Причина:', value=reason)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=user.avatar)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='kick', description='Мне он не нравится, его я выгоняю!')
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member, reason):
        guild = inter.guild

        await guild.kick(user, reason)
        E = disnake.Embed(title='🔖 Нарушитель был кикнут', color=0xff0000)
        E.add_field(name='Администратор:', value=inter.author.mention)
        E.add_field(name='Нарушитель:', value=user.mention)
        E.add_field(name='Причина:', value=reason)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=user.avatar)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='warn', description='Пожалуйста, не делай так больше!')
    @commands.has_permissions(moderate_members=True)
    async def warn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        cursor.execute('SELECT w_count FROM warns WHERE guild_name = ? AND user_id = ?', (inter.guild.name, member.id))
        row = cursor.fetchone()

        if row:
            count = row[0]
        else:
            count = 0

        count += 1

        if count == 1:
            cursor.execute('INSERT INTO warns (guild_name, user_id, w_count) VALUES (?, ?, ?)', (inter.guild.name, member.id, count))
            conn.commit()
        else:
            cursor.execute('UPDATE warns SET w_count = ? WHERE guild_name = ? AND user_id = ?', (count, inter.guild.name, member.id))
            conn.commit()

        E = disnake.Embed(title='🚨 Участник вечеринки получил предупреждение!', color=0xf4a676)
        E.add_field(name='Администратор:', value=inter.author.mention)
        E.add_field(name='Нарушитель:', value=member.mention)
        if reason:
            E.add_field(name='Причина:', value=reason)
        else:
            pass
        E.add_field(name='Количество варнов:', value=count)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='unwarn', description='Я прощаю тебя.')
    @commands.has_permissions(moderate_members=True)
    async def unwarn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, count: int):
        if count <= 0:
            raise commands.CommandError(message='Указано отрицательное значение количества или ноль.')
        else:
            cursor.execute('SELECT w_count FROM warns WHERE guild_name = ? AND user_id = ?', (inter.guild.name, member.id))
            row = cursor.fetchone()

            if row:
                warning_count = row[0]
            else:
                warning_count = 0

            if warning_count == 0:
                raise commands.CommandError(message='У пользователя нет варнов.')
            if count >= warning_count:
                cursor.execute('DELETE FROM warns WHERE guild_name = ? AND user_id = ?', (inter.guild.name, member.id))
                conn.commit()
                
                embed1 = disnake.Embed(
                    title="🎌 С пользователя сняты все обвинения!",
                    color=0xf8b952
                )
                embed1.add_field(name='Администратор:', value=inter.author.mention)
                embed1.add_field(name='Участник:', value=member.mention)
                embed1.add_field(name='Снято варнов:', value='Все варны сняты')
                embed1.add_field(name='Количество варнов:', value='0')
                embed1.set_footer(text=random.choice(footer), icon_url=inter.author.avatar)
                await inter.response.send_message(embed=embed1)
            else:
                warning_count -= count
                cursor.execute('UPDATE warns SET w_count = ? WHERE guild_name = ? AND user_id = ?', (warning_count, inter.guild.name, member.id))
                conn.commit()

                embed = disnake.Embed(
                    title="🎌 С пользователя сняты обвинения!",
                    color=0xf8b952
                )
                embed.add_field(name='Администратор:', value=inter.author.mention)
                embed.add_field(name='Участник:', value=member.mention)
                embed.add_field(name='Снято варнов:', value=count)
                embed.add_field(name='Количество варнов:', value=warning_count)
                embed.set_footer(text=random.choice(footer), icon_url=inter.author.avatar)
                await inter.response.send_message(embed=embed)

    @moderation.sub_command(name='lockdown', description='Блокируйте все чаты ради безопасности!')
    @commands.has_permissions(administrator=True)
    async def lock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        guild = inter.guild
        channels = await guild.fetch_channels()

        cursor.execute('SELECT role_id FROM lkroles WHERE guild_id = ?', (guild.id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise commands.CommandError(message='Роль, которой нужно запретить говорить, не найдена или полностью отсуствует.')
        else:
            role = guild.get_role(role_id[0])
        if role:
            for channel in channels:
                await channel.set_permissions(role, send_messages=False)

            E = disnake.Embed(title='🛑 На сервере введено чрезвычайное положение', color=0xff0000)
            E.add_field(name='Что случилось?', value=f'```Администратор сервера запретил отправлять сообщения во все каналы для роли "{role.name}".```')
            E.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await inter.followup.send(embed=E)
        else:
            raise commands.CommandError(message='Роль, которой нужно запретить говорить, не найдена или полностью отсуствует.')

    @moderation.sub_command(name='unlock', description='Блокируйте все чаты ради безопасности!')
    @commands.has_permissions(administrator=True)
    async def unlock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()

        guild = inter.guild
        channels = await guild.fetch_channels()

        cursor.execute('SELECT role_id FROM lkroles WHERE guild_id = ?', (guild.id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise commands.CommandError(message='Роль, которой нужно разрешить говорить, не найдена или полностью отсуствует.')
        else:
            role = guild.get_role(role_id[0])
        if role:
            for channel in channels:
                await channel.set_permissions(role, send_messages=None)

            E = disnake.Embed(title='🩷 Чрезвычайное положение отменено', color=0x8eff77)
            E.add_field(name='Что случилось?', value=f'```Администратор сервера вновь разрешил общение в каналах сервера для роли "{role.name}".```')
            E.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await inter.followup.send(embed=E)
        else:
            raise commands.CommandError(message='Роль, которой нужно разрешить говорить, не найдена или полностью отсуствует.')

    @moderation.sub_command(name='clear', description='Как много мусора... Но я могу очистить его!')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.ApplicationCommandInteraction, amount: int):
        if amount <= 0:
            m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Произошла ошибка при исполнении команды.", color=0xff6969)
            m1.add_field(name="От чего все проблемы?", value=f"```Вы указали отрицательное значение или ноль.```")
            m1.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar.url)
            await inter.response.send_message(embed=m1)
            return
        
        elif amount >= 75:
            m1 = disnake.Embed(title="⚠️ Произошла ошибка!", description="Произошла ошибка при исполнении команды.", color=0xff6969)
            m1.add_field(name="От чего все проблемы?", value=f"```Вы указали слишком большое значение.```")
            m1.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar.url)
            await inter.response.send_message(embed=m1)
            return

        messages = await inter.channel.history(limit=amount).flatten()
        messages = [msg for msg in messages if msg.id != inter.id]
        await inter.channel.delete_messages(messages)

        embed = disnake.Embed(title="✨ Чат очищен!", description=f"Было вынесено **{amount}** пакетов мусора.", color=0x50c878)
        author = inter.author
        embed.set_footer(text=f"Спасибо, что помог с уборкой, {author.name}! <3", icon_url=author.avatar.url)
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ModCog(bot))