import asyncio
import platform
import random
import sqlite3
import disnake
from disnake.ext import commands
from disnake import ui
from core.utilities.embeds import footer
from cogs.events.locale import Locale

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
    CREATE TABLE IF NOT EXISTS ages (
        user_id INTEGER PRIMARY KEY,
        age INTEGER
    )
''')
conn.commit()

class UtilitiesCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.locale = Locale(bot)

    @commands.slash_command(description='Утилиты, а ты что думал?')
    async def utilities(self, inter):
        ...

    @commands.command()
    async def stats(self, inter: disnake.CommandInteraction):
        formatted_time = f"<t:{int(self.bot.start_time)}:R>"
        commands = len(inter.bot.commands) + len(inter.bot.slash_commands)
        guilds = len(self.bot.guilds)
        users = len(self.bot.users)

        stats = await self.locale.get_translation(inter.author.id, "stats")
        footer = await self.locale.get_translation(inter.author.id, "footer")

        main = [
            stats[2].format(formatted_time=formatted_time),
            stats[3],
            stats[4].format(latency=round(self.bot.latency * float(1000))),
            stats[5].format(commands=commands),
            stats[6].format(guilds=guilds),
            stats[7].format(users=users)
        ]

        E = disnake.Embed(title=stats[0], color=disnake.Color.random())
        E.add_field(name=f'> {stats[1]}', value=''.join(main), inline=False)
        E.set_author(name=self.bot.owner.name, icon_url=self.bot.owner.avatar)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=self.bot.user.avatar)
        await inter.send(embed=E)

    @utilities.sub_command(name='server', description='Статистика вашего сервера.')
    async def server(self, inter: disnake.ApplicationCommandInteraction):
        #какой-то мусор (для вывода естественно)
        guild = inter.guild
        author = inter.author
        region = inter.guild.preferred_locale
        members = inter.guild.member_count
        mfa_lvl = inter.guild.mfa_level
        verification = inter.guild.verification_level
        max_members = inter.guild.max_members
        roles = len(guild.roles)
        boost_role = inter.guild.premium_subscriber_role
        boosters = guild.premium_subscription_count
        boost_tier = guild.premium_tier
        boost_progress = guild.premium_progress_bar_enabled
        channels = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        emojis = len(guild.emojis)
        stikers = len(guild.stickers)

        if boost_progress == False:
            boost_progress = 'Выключен'
        if boost_progress == True:
            boost_progress = 'Включен'

        if mfa_lvl == 0:
            mfa_lvl = "Выключена"
        else:
            mfa_lvl= "Включена"

        about_guild = (
            f'Владелец: **{guild.owner.name}**',
            f'ID сервера: **{guild.id}**',
            f'Регион: **{region}**',
            f'Уровень проверки: **{verification}**',
            f'Двухфакторная Аутентификация: **{mfa_lvl}**',
        )

        roles = (
            f'Ролей: **{roles}**',
            f'Ваша высшая роль: **{author.top_role.mention}**',
            f'Роль поддержавших: **{boost_role.mention if boost_role else "Роль отсутствует."}**',
        )

        channels_and_boosts = (
            f'Прогресс Бар: **{boost_progress}**',
            f'Поддержавших: **{boosters or "Поддержавших нет."}**',
            f'Уровень поддержки: **{boost_tier}**',
            f'---------------------------------',
            f'Всего каналов: **{channels}**',
            f'Текстовых каналов: **{text_channels}**',
            f'Голосовых каналов: **{voice_channels}**',
        )

        other = (
            f'Участников: **{members}**',
            f'Стикеры: **{stikers}**',
            f'Эмодзи: **{emojis}**',
            f'Максимальное кол-во участников: **{max_members}**',
            f'Ботов: **{len(([member for member in guild.members if member.bot]))}**',
        )

        emb = disnake.Embed(title=f"Информация о сервере {guild.name}", description=guild.description or 'Описание отсутствует.', color=disnake.Color.random())
        emb.add_field(name="> О сервере:", value='\n'.join(about_guild), inline=False)
        emb.add_field(name="> Роли:", value='\n'.join(roles), inline=False)
        emb.add_field(name="> Каналы и Бусты:", value='\n'.join(channels_and_boosts), inline=False)
        emb.add_field(name="> Прочее:", value='\n'.join(other), inline=False)

        if guild.banner:
            emb.set_image(url=guild.banner)
        else:
            pass
            
        emb.set_thumbnail(url=guild.icon)
        await inter.response.send_message(embed = emb)

    @utilities.sub_command(name='emoji', description='Укради эмодзи!')
    @commands.has_permissions(manage_emojis=True)
    async def steal(self, inter: disnake.ApplicationCommandInteraction, emoji: disnake.PartialEmoji, name: str = None):
        guild = inter.guild

        #читаем полученный эмодзи и его имя
        emoji_bytes = await emoji.read()
        emoji_name = name or emoji.name

        #проверяем, есть ли на сервере эмодзи с похожим именем
        if any(emoji_name.lower() == existing_emoji.name.lower() for existing_emoji in guild.emojis):
            raise commands.CommandError(message='Это имя для эмодзи уже существует на этом сервере.')
        else:
            new_emoji = await guild.create_custom_emoji(name=emoji_name, image=emoji_bytes)
            E = disnake.Embed(
                title='💫 Эмодзи добавлен!',
                color=0xb1ff98
            )
            E.add_field(name='Ответ команды:', value=f'```Эмодзи, который вы указали, был добавлен на эту вечеринку с именем {emoji_name}.```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
    
    @commands.command(description='Помогу вывести информацию о всех пользователях Discord.')
    async def user(self, ctx, user: disnake.User = None):
        author = ctx.author
        if user is None:
            user = author
        
        banner = await self.bot.fetch_user(user.id)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'

        cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            prefix = row[0]
        else:
            prefix = "px-"

        cursor.execute("SELECT * FROM blacklist WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()

        if result:
            blacklist = 'Да'
        else:
            blacklist = 'Нет'

        all_info = (
            f"**💫  |  ID: __{user.id}__**",
            f'**🌍  |  Работоспособен: {created_at_indicator}**',
            f'**🚫  |  Чёрный список: __{blacklist}__**'
        )

        settings = [
            f'**⭐ | Префикс: __{prefix}__**',
            f'**🩷 | Статус: __Скоро...__**'
        ]

        emb = disnake.Embed(color=disnake.Color.random())
        emb.add_field(name='Общая ифнормация', value='\n'.join(all_info), inline=False)
        emb.add_field(name='Используемые данные', value='\n'.join(settings), inline=False)
        emb.set_author(name=user.name, icon_url=user.avatar)

        if banner and banner.banner:
            emb.set_image(url=banner.banner.url)
        if banner is None:
            return
        
        emb.set_thumbnail(url=user.avatar)
        await ctx.reply(embed=emb)

    @commands.command(description="Информация об участнике сервера.")
    async def profile(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member | disnake.User = None):
        if user is None:
            user = inter.author

        cursor.execute("SELECT * FROM blacklist WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()

        if result:
            blacklist = 'Да'
        else:
            blacklist = 'Нет'

        activity = 'Активность отсутствует.'
        bot = user.bot

        if bot == True:
            boy = 'Да'
        else:
            boy = 'Нет'
        
        if user.activity:
            if user.activity.type == disnake.ActivityType.playing:
                activity = f"🎮 Играет в {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.streaming:
                activity = f"📟 Стримит {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.listening:
                activity = f"🎧 Слушает {user.activity.name}"
            elif user.activity.type == disnake.ActivityType.watching:
                activity = f"👁️ Смотрит {user.activity.name}"
            else:
                activity = user.activity
        
        banner = await self.bot.fetch_user(user.id)

        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:R>'
        joined_at_indicator = f'<t:{int(user.joined_at.timestamp())}:R>'

        cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            prefix = row[0]
        else:
            prefix = "px-"

        cursor.execute('SELECT age FROM ages WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        if row:
            age = row[0]
        else:
            age = "Не указан."

        user_info = (
            f"**🪪  |  ID: __{user.id}__**",
            f'**📔  |  В списке: __{created_at_indicator}__**',
            f'**🔖  |  Статус: __Скоро...__**',
            f'**🛑  |  Чёрный список: __{blacklist}__**',
        )

        other_info = (
            f'**🎭  |  Высшая роль: __{user.top_role.mention}__**',
            f'**🌌  |  Аватар: __[Открыть]({user.avatar.url})__**',
        )

        babax_info = (
            f'**📟  |  Положение: __{user.status}__**',
            f'**🤖  |  Бот: __{boy}__**',
            f'**⭐  |  Веселится: __{joined_at_indicator}__**',
        )

        database_info = (
            f'**💾  |  Префикс: __{prefix}__**',
            f'**🔞  |  Возраст: __{age}__**',
        )

        if banner and banner.banner:
            other_info += (f'**🎌  |  Баннер: __[Открыть]({banner.banner.url})__**', )

        view = ProfileMenu(self.bot, inter.author.id)

        if user.id != inter.author.id:
            view.children = []

            view.bot = self.bot

        emb = disnake.Embed(title=f'Профиль участника {user.name}', description=activity, color=disnake.Color.random())
        emb.add_field(name="> Всё об участнике", value='\n'.join(user_info), inline=False)  
        emb.add_field(name='> Статистика пользователя', value='\n'.join(babax_info))
        emb.add_field(name='> Прочее', value='\n'.join(other_info))
        emb.add_field(name='> Общие сведения', value='\n'.join(database_info), inline=False) 
        emb.set_author(name=user.name, icon_url=user.avatar)

        if banner and banner.banner:
            emb.set_image(url=banner.banner.url)
        if banner is None:
            return
        
        emb.set_thumbnail(url=user.avatar)
        await inter.reply(embed=emb, view=view)

class ProfileMenu(ui.View):
    def __init__(self, bot, author_id):
        super().__init__()
        self.timeout = 20
        self.age = None
        self.bot = bot
        self.author_id = author_id

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user.id == self.author_id
    
    @ui.button(label='Указать возраст', style=disnake.ButtonStyle.green)
    async def set_age(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        try:
            age_msg = await inter.channel.send('У вас есть 20 секунд для указания возраста. Помни, что мы не принимаем на вечеринку тех, кто младше 13-ти лет и старше 99-ти.')

            def check_age(m):
                return m.author == inter.user and m.channel == age_msg.channel
            
            age_response = await self.bot.wait_for('message', check=check_age, timeout=self.timeout)

            if age_response.content.isdigit() and 13 <= int(age_response.content) < 100:
                self.age = int(age_response.content)
                await age_msg.delete()
                await age_response.add_reaction("✅")

                cursor.execute('INSERT OR REPLACE INTO ages VALUES (?, ?)', (inter.user.id, self.age))
                conn.commit()
            elif int(age_response.content) < 13:
                await age_msg.delete()
                raise commands.CommandError(message='Ты как на платформе зарегистрировался, мальчик?')
            elif int(age_response.content) > 100:
                await age_msg.delete()
                raise commands.CommandError(message='Ты ветеран что-ли?')

        except asyncio.TimeoutError:
            await age_msg.delete()
            raise commands.CommandError(message='Вы не успели указать возраст.')

def setup(bot: commands.Bot):
    bot.add_cog(UtilitiesCog(bot))