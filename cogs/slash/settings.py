import random
import disnake
from disnake.ext import commands
import sqlite3
from core.utilities.embeds import footer
from cogs.events.locale import Locale

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS locales (
            user_id TEXT PRIMARY KEY, 
            language TEXT
             )
        ''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS voices (
    guild_id INTEGER PRIMARY KEY,
    channel_id INTEGER
    )
''')
conn.commit()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS user_voices (
    id INTEGER PRIMARY KEY,
    guild_id INTEGER,
    user_id INTEGER,
    channel_id INTEGER
    )
''')
conn.commit()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS logs (
               guild_id INTEGER PRIMARY KEY,
               channel_id INTEGER
               )
''')
conn.commit()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS auto_roles (
               guild_id INTEGER PRIMARY KEY,
               guild_name TEXT,
               role_id INTEGER
               )
               ''')
conn.commit()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS prefix (
               user_id INTEGER PRIMARY KEY,
               prefix_name TEXT
               )
               ''')
conn.commit()

cursor.execute('''
         CREATE TABLE IF NOT EXISTS autothread (
               id INTEGER PRIMARY KEY,
               guild_id INTEGER NOT NULL,
               guild_name TEXT,
               channel_id INTEGER NOT NULL
)
''')
conn.commit()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS atembed (
               id INTEGER PRIMARY KEY,
               guild_id INTEGER NOT NULL,
               guild_name TEXT,
               channel_id INTEGER NOT NULL,
               name TEXT,
               title TEXT,
               description TEXT,
               color INTEGER
)
''')
conn.commit()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS lkroles (
            guild_id INTEGER PRIMARY KEY,
            role_id INTEGER
        )
''')

class SettingsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.locale = Locale(bot)

    @commands.slash_command(description="Настрой-ка меня, Сен-пай u-u.")
    async def settings(self, inter):
        ...

    @commands.slash_command(description='Организуйте мне голосовуху. / Organize a voice for me.')
    async def voice(self, inter):
        ...

    @settings.sub_command(name='logs', description='Буду пересматривать наш праздник вечность!')
    @commands.has_permissions(administrator=True)
    async def logs(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить/Изменить канал', 'Удалить канал']), channel: disnake.TextChannel = None):
        guild_id = inter.guild.id

        if action == 'Установить/Изменить канал':
            if channel:
                cursor.execute('SELECT channel_id FROM logs WHERE guild_id = ?', (guild_id,))
                exc_channel_id = cursor.fetchone()

            if exc_channel_id:
                cursor.execute('UPDATE logs SET channel_id = ? WHERE guild_id = ?', (channel.id, guild_id))
                conn.commit()

                titl = '🔄️ Канал логов изменён'
                act = 'Установлен в качестве замены прошлого канала.'
                clr = 0xF2FC58
            else:
                cursor.execute('INSERT INTO logs (guild_id, channel_id) VALUES (?, ?)', (guild_id, channel.id))
                conn.commit()

                titl = '✅ Канал логов установлен'
                act = 'Установлен как новый канал логов.'
                clr = 0x84FE9A

            E = disnake.Embed(title=titl, color=clr)
            E.add_field(name='Название канала:', value=channel.mention)
            E.add_field(name='Действие:', value=act)
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
        
        elif action == 'Удалить канал' and channel is None:
            cursor.execute('DELETE FROM logs WHERE guild_id = ?', (guild_id,))
            conn.commit()

            E = disnake.Embed(title='🚫 Канал логов удалён.', color=0xe52f07)
            E.add_field(name='Ответ команды:', value=f'```Изменения на этом сервере более не будут отображаться.```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)

    @voice.sub_command(name='create', description='Голосовой для голосовых? Звучит... странно. / Voice for voice? Sounds... weird.')
    @commands.has_permissions(manage_channels=True)
    async def create(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Создать / Create', 'Удалить / Delete']), *, channel_name: str = 'Создать голосовой канал'):
        await inter.response.defer()
        guild = inter.guild

        if action == 'Создать / Create':
            chan = await guild.create_voice_channel(name=channel_name, user_limit=1)

            cursor.execute('INSERT INTO voices (guild_id, channel_id) VALUES (?, ?)', (guild.id, chan.id))
            conn.commit()

            voice = await self.locale.get_translation(inter.author.id, 'voice_create')
            footer = await self.locale.get_translation(inter.author.id, 'footer')

            E = disnake.Embed(title=voice['title'], color=0xd0f594)
            E.add_field(name='', value=voice['field'].format(channel_mention=chan.mention))
            E.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await inter.followup.send(embed=E)

        else:
            cursor.execute('SELECT channel_id FROM voices WHERE guild_id = ?', (guild.id,))
            chan = cursor.fetchone()
            chan2 = chan[0]

            channel = guild.get_channel(chan2)
            cursor.execute('DELETE FROM voices WHERE guild_id = ?', (guild.id,))
            conn.commit()
            await channel.delete()
            await inter.followup.send('✅', ephemeral=True)

    @voice.sub_command(name='join', description='Ну не будете же вы один сидеть, да? / Well, you won’t sit alone, right?')
    async def allow(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Разрешить вход / Allow join', 'Запретить вход / Deny join']), *, user: disnake.Member):
        cursor.execute('SELECT channel_id FROM user_voices WHERE guild_id = ? AND user_id = ?', (inter.guild.id, inter.author.id))
        channel_row = cursor.fetchone()

        if channel_row:
            channel_id = channel_row[0]

            voice = await self.locale.get_translation(inter.author.id, 'voice_allow_deny')

            if action == 'Разрешить вход / Allow join':
                chan = inter.guild.get_channel(channel_id)
                await chan.set_permissions(user, move_members=True, speak=True)
                await inter.response.send_message(voice['allow'].format(user=user.mention, channel=chan.mention))

            elif action == 'Запретить вход / Deny join':
                chan = inter.guild.get_channel(channel_id)
                await chan.set_permissions(user, move_members=False, speak=True)
                await inter.response.send_message(voice['deny'])

        else:
            await inter.response.send_message(voice['no_channel'])

    @settings.sub_command(name='user-lang', description="Хочешь, будем общаться на французском? / Do you want us to communicate in French?")
    async def set_lang(self, inter: disnake.ApplicationCommandInteraction, language: str = commands.Param(choices=['Русский', 'English'])):
        language_code = "ru" if language.lower() == "русский" else "en"
        cursor.execute("REPLACE INTO locales (user_id, language) VALUES (?, ?)",
                       (str(inter.author.id), language_code))
        conn.commit()

        trans = await self.locale.get_translation(inter.author.id, 'locale')
        footer = await self.locale.get_translation(inter.author.id, "footer")

        E = disnake.Embed(title=trans[0], color=0x9bf8e0)
        E.add_field(name=trans[1], value=f'```{trans[2].format(language=language)}```')
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=E, ephemeral=True)

    @settings.sub_command(name='autorole', description='Статусы для гостей? Как мило!')
    @commands.has_permissions(administrator=True)
    async def auto_role(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить/Изменить роль', 'Удалить роль']), *, role: disnake.Role = None):
        guild_id = inter.guild.id
        guild_name = inter.guild.name

        if action == 'Установить/Изменить роль':
            if role:
                cursor.execute('SELECT role_id FROM auto_roles WHERE guild_id = ?', (guild_id,))
                role_id = cursor.fetchone()

            if role_id:
                cursor.execute('UPDATE auto_roles SET role_id = ? WHERE guild_id = ?', (role.id, guild_name))
                conn.commit()

                titl = '🔄️ Авто-роль переопределена.'
                act = f'{role.mention} была установлена, как новая авто-роль.'
                clr = 0xF2FC58
            else:
                cursor.execute('INSERT INTO auto_roles (guild_id, guild_name, role_id) VALUES (?, ?, ?)', (guild_id, guild_name, role.id))
                conn.commit()

                titl = '✅ Авто-роль установлена.'
                act = f'{role.mention} теперь будет выдаваться каждому новому участнику вечеринки.'
                clr = 0x84FE9A

            E = disnake.Embed(title=titl, color=clr)
            E.add_field(name='Установленная роль:', value=role.mention)
            E.add_field(name='Действие:', value=act)
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
        
        elif action == 'Удалить роль' and role is None:
            cursor.execute('DELETE FROM auto_roles WHERE guild_id = ?', (guild_id,))
            conn.commit()

            E = disnake.Embed(title='🚫 Авто-роль удалена.', color=0xe52f07)
            E.add_field(name='Ответ команды:', value=f'```Новые участники вечеринки больше не будут получать роль при посещении.```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)

    @settings.sub_command(name='lockdown-role', description='А кому я собственно запрещу разговаривать?')
    @commands.has_permissions(administrator=True)
    async def ldrole(self, inter: disnake.ApplicationCommandInteraction, role: disnake.Role):
        await inter.response.defer()

        cursor.execute('SELECT role_id FROM lkroles WHERE guild_id = ?', (inter.guild.id,))
        r1 = cursor.fetchone()

        if r1:
            cursor.execute('UPDATE lkroles SET role_id = ? WHERE guild_id = ?', (role.id, inter.guild.id))
            conn.commit

            E = disnake.Embed(title='🟢 Роль успешно назначена', color=0x8eff77)
            E.add_field(name='Ответ команды:', value=f'```Теперь роль "{role.name}" будет подвержена блокировке (в каналах имеется в виду, а вы о чём подумали?).```')
            E.set_footer(text=random.choice(footer), icon_url=inter.guild.icon)
            await inter.followup.send(embed=E)
        else:
            cursor.execute('INSERT INTO lkroles (guild_id, role_id) VALUES (?, ?)', (inter.guild.id, role.id))
            conn.commit()
            
            E = disnake.Embed(title='🟢 Роль успешно назначена', color=0x8eff77)
            E.add_field(name='Ответ команды:', value=f'```Теперь роль "{role.name}" будет подвержена блокировке (в каналах имеется в виду, а вы о чём подумали?).```')
            E.set_footer(text=random.choice(footer), icon_url=inter.guild.icon)
            await inter.followup.send(embed=E)

    @settings.sub_command(name='prefix', description='Хотите придумать для меня позывной?')
    async def prefix(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить/Изменить префикс', 'Удалить префикс']), *, prefix: str = None):
        if action == 'Установить/Изменить префикс':
            if prefix:
                cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (inter.author.id, ))
                prefix_name = cursor.fetchone()

            if prefix_name:
                cursor.execute('UPDATE prefix SET prefix_name = ? WHERE user_id = ?', (prefix, inter.author.id))
                conn.commit()

                titl = '🔄️ Префикс переопределён.'
                act = f'{prefix} был установлен, как новый префикс для вас.'
                clr = 0xF2FC58
            else:
                cursor.execute('INSERT INTO prefix (user_id, prefix_name) VALUES (?, ?)', (inter.author.id, prefix))
                conn.commit()

                titl = '✅ Авто-роль установлена.'
                act = f'Теперь, при помощи {prefix} вы сможете использовать мои команды.'
                clr = 0x84FE9A

            E = disnake.Embed(title=titl, color=clr)
            E.add_field(name='Установленный префикс:', value=prefix, inline=False)
            E.add_field(name='Действие:', value=act)
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E, ephemeral=True)

        elif action == 'Удалить префикс' and prefix is None:
            cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (inter.author.id, ))
            prefix_n1 = cursor.fetchone()

            if prefix_n1:
                cursor.execute('DELETE FROM prefix WHERE user_id = ?', (inter.author.id,))
                conn.commit()

                E = disnake.Embed(title='🚫 Префикс удален.', color=0xe52f07)
                E.add_field(name='Ответ команды:', value=f'```Отныне основной префикс вновь px-```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E, ephemeral=True)

    @settings.sub_command(name='autothread', description='Автоматические ветки? Звучит хайпово!')
    @commands.has_permissions(manage_channels=True)
    async def thread(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить новый канал', 'Удалить канал']), *, channel: disnake.TextChannel):
        guild_id = inter.guild.id
        guild_name = inter.guild.name

        if action == 'Установить новый канал':
            cursor.execute('INSERT INTO autothread (guild_id, guild_name, channel_id) VALUES (?, ?, ?)', (guild_id, guild_name, channel.id))
            conn.commit()

            E = disnake.Embed(title='✅ Автоветки установлены', color=0x84FE9A)
            E.add_field(name='Название канала:', value=channel.mention)
            E.add_field(name='Действие:', value='```Установлен как канал для автоматических веток.```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)

        elif action == 'Удалить канал':
            cursor.execute('SELECT channel_id FROM atembeds WHERE guild_id = ? AND channel_id = ?', (guild_id, channel.id))
            exc_channel_id = cursor.fetchone()

            if exc_channel_id is None:
                E = disnake.Embed(title='⚠️ Ошибочка вышла!', color=0xe52f07)
                E.add_field(name='Почему я вас динамлю?..', value=f'```Указанный канал не является каналом для автоматических веток.```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E, ephemeral=True)
                return
            else:
                cursor.execute('DELETE FROM atembeds WHERE guild_id = ? AND channel_id = ?', (guild_id, channel.id))
                conn.commit()

                E = disnake.Embed(title='🚫 Автоветки удалены.', color=0xe52f07)
                E.add_field(name='Ответ команды:', value=f'```Указанный канал для автоматических веток был успешно удален.```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E)
                return
            
    @settings.sub_command(name='autothread-embed', description='Давайте настроим эмбед вам по вкусу!')
    @commands.has_permissions(manage_channels=True)
    async def atembeds(self, inter: disnake.ApplicationCommandInteraction, action: str = commands.Param(choices=['Установить', 'Удалить']), *, channel: disnake.TextChannel, name: str = None, title: str = None, description: str = None, color: str = None):
        if action == 'Установить' and name != None and title != None and color != None:
            cursor.execute('SELECT channel_id FROM atembed WHERE guild_id = ? AND channel_id = ?', (inter.guild.id, channel.id))
            check = cursor.fetchone()

            if check:
                cursor.execute('DELETE FROM atembed WHERE guild_id = ? AND channel_id = ?', (inter.guild.id, channel.id))
                conn.commit()

            cursor.execute('INSERT INTO atembed (guild_id, guild_name, channel_id, name, title, description, color) VALUES (?, ?, ?, ?, ?, ?, ?)', (inter.guild.id, inter.guild.name, channel.id, name, title, description, color))
            conn.commit()

            E = disnake.Embed(title='✅ Эмбед настроен!', color=0x84FE9A)
            E.add_field(name='Название канала:', value=channel.mention)
            E.add_field(name='Действие:', value='```Заголовок, Описание и Цвет эмбеда были установлены для ветки.```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
        
        if action == 'Удалить' and name == None and title == None and description == None and color == None:
            cursor.execute('SELECT channel_id FROM atembed WHERE guild_id = ? AND channel_id = ?', (inter.guild.id, channel.id))
            exc_channel_id = cursor.fetchone()

            if exc_channel_id is None:
                E = disnake.Embed(title='⚠️ Ошибочка вышла!', color=0xe52f07)
                E.add_field(name='Почему я вас динамлю?..', value=f'```Указанный канал не является каналом для автоматических веток.```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E, ephemeral=True)
                return
            else:
                cursor.execute('DELETE FROM atembed WHERE guild_id = ? AND channel_id = ?', (inter.guild.id, channel.id))
                conn.commit()

                E = disnake.Embed(title='🚫 Оформление удалено.', color=0xe52f07)
                E.add_field(name='Ответ команды:', value=f'```Указанное ранее оформление заменено стандартным.```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E)
                return

def setup(bot: commands.Bot):
    bot.add_cog(SettingsCog(bot))