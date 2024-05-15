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

    @utilities.sub_command(name='statistics', description='Моё самочувствие / My health')
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

    @utilities.sub_command(name='server', description='Статистика вашего сервера. / Your server stats.')
    async def server(self, inter: disnake.ApplicationCommandInteraction):
        # Получаем данные о сервере
        guild = inter.guild
        author = inter.author
        region = inter.guild.preferred_locale
        members = inter.guild.member_count
        mfa_lvl = inter.guild.mfa_level
        verification = inter.guild.verification_level
        max_members = inter.guild.max_members
        roles_count = len(guild.roles)
        boost_role = inter.guild.premium_subscriber_role
        boosters = guild.premium_subscription_count
        boost_tier = guild.premium_tier
        boost_progress = guild.premium_progress_bar_enabled
        channels = len(guild.channels)
        text_channels = len(guild.text_channels)
        voice_channels = len(guild.voice_channels)
        emojis = len(guild.emojis)
        stickers = len(guild.stickers)

        guild_info_translations = await self.locale.get_translation(inter.author.id, "guild_info")
        roles_translations = await self.locale.get_translation(inter.author.id, "roles")
        channels_and_boosts_translations = await self.locale.get_translation(inter.author.id, "channels_and_boosts")
        other_translations = await self.locale.get_translation(inter.author.id, "other")
        fields_translations = await self.locale.get_translation(inter.author.id, 'server_info_fields')
        title_translations = await self.locale.get_translation(inter.author.id, 'server_info_title')
        description_translation = await self.locale.get_translation(inter.author.id, 'server_info_description')
        mfa_boost = await self.locale.get_translation(inter.author.id, 'mfa_boost')

        boost_progress_text = mfa_boost['boost_enabled'] if boost_progress else mfa_boost['boost_disabled']
        mfa_lvl_text = mfa_boost['mfa_enabled'] if mfa_lvl else mfa_boost['mfa_disabled']

        about_guild = (
            guild_info_translations["owner"].format(owner_name=guild.owner.name),
            guild_info_translations["guild_id"].format(guild_id=guild.id),
            guild_info_translations["region"].format(region=region),
            guild_info_translations["verification_level"].format(verification=verification),
            guild_info_translations["mfa_authentication"].format(mfa_lvl=mfa_lvl_text)
        )

        roles = (
            roles_translations["total_roles"].format(roles=roles_count),
            roles_translations["highest_role"].format(top_role=author.top_role.mention),
            roles_translations["boost_role"].format(boost_role=boost_role.mention if boost_role else "Not found.")
        )

        channels_and_boosts = (
            channels_and_boosts_translations["progress_bar"].format(boost_progress=boost_progress_text),
            channels_and_boosts_translations["boosters"].format(boosters=boosters or "No one support this server."),
            channels_and_boosts_translations["boost_tier"].format(boost_tier=boost_tier),
            "---------------------------------",
            channels_and_boosts_translations["channel_count"].format(channels=channels),
            channels_and_boosts_translations["text_channels"].format(text_channels=text_channels),
            channels_and_boosts_translations["voice_channels"].format(voice_channels=voice_channels)
        )

        other = (
            other_translations["members"].format(members=members),
            other_translations["stickers"].format(stickers=stickers),
            other_translations["emojis"].format(emojis=emojis),
            other_translations["max_members"].format(max_members=max_members),
            other_translations["bots"].format(bot_count=len([member for member in guild.members if member.bot]))
        )

        emb = disnake.Embed(title=f"{title_translations.format(guild_name=guild.name)}", description=description_translation.format(guild_description=guild.description) or 'Description is None.', сolor=disnake.Color.random())
        emb.add_field(name=f"> {fields_translations['server']}", value='\n'.join(about_guild), inline=False)
        emb.add_field(name=f"> {fields_translations['roles']}", value='\n'.join(roles), inline=False)
        emb.add_field(name=f"> {fields_translations['channels_and_boosts']}", value='\n'.join(channels_and_boosts), inline=False)
        emb.add_field(name=f"> {fields_translations['other']}", value='\n'.join(other), inline=False)

        if guild.banner:
            emb.set_image(url=guild.banner)

        emb.set_thumbnail(url=guild.icon)
        await inter.response.send_message(embed=emb)

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
    
    @utilities.sub_command(name='user', description='Помогу вывести информацию о всех пользователях Discord.')
    async def user(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        author = inter.author
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
        await inter.response.send_message(embed=emb)

    @utilities.sub_command(description="Информация об участнике сервера. / Information about server member.")
    async def profile(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member | disnake.User = None):
        blacklist_translation = await self.locale.get_translation(inter.author.id, "blacklist")
        activity_translation = await self.locale.get_translation(inter.author.id, "activity")
        bot_translation = await self.locale.get_translation(inter.author.id, "bot")
        prefix_translation = await self.locale.get_translation(inter.author.id, "prefix")

        if user is None:
            user = inter.author

        cursor.execute("SELECT * FROM blacklist WHERE user_id = ?", (user.id,))
        result = cursor.fetchone()

        if result:
            blacklist = blacklist_translation[0]
        else:
            blacklist = blacklist_translation[1]

        if user.bot == 'True':
            boy = bot_translation[0]
        else:
            boy = bot_translation[1]

        bot = bot_translation[int(user.bot)]

        banner = await self.bot.fetch_user(user.id)

        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:R>'
        joined_at_indicator = f'<t:{int(user.joined_at.timestamp())}:R>'

        cursor.execute('SELECT language FROM locales WHERE user_id = ?', (user.id,))
        langg = cursor.fetchone()

        if langg:
            langg = langg[0]
            if langg == 'ru':
                lang = 'Русский'
            elif langg == 'en':
                lang = 'English'
            else:
                lang = 'Unknown language'
        else:
            lang = 'Unknown language'

        cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        prefix = row[0] if row else prefix_translation

        '''cursor.execute('SELECT age FROM ages WHERE user_id = ?', (user.id,))
        row = cursor.fetchone()
        age = row[0] if row else age_not_specified_translation'''

        user_info = await self.locale.get_translation(inter.author.id, "user_info")
        other_info = await self.locale.get_translation(inter.author.id, "other_info")
        babax_info = await self.locale.get_translation(inter.author.id, "babax_info")
        database_info = await self.locale.get_translation(inter.author.id, "database_info")
        profile = await self.locale.get_translation(inter.author.id, 'profile')

        user_info_formatted = (
            f"**{user_info[0].format(user_id=user.id)}**",
            f"**{user_info[1].format(created_at_indicator=created_at_indicator)}**",
            f"**{user_info[2]}**",
            f"**{user_info[3].format(blacklist=blacklist)}**"
        )

        other_info_formatted = (
            f"**{other_info[0].format(top_role_mention=user.top_role.mention)}**",
            f"**{other_info[1].format(avatar_url=user.avatar.url)}**"
        )

        babax_info_formatted = (
            f"**{babax_info[0].format(status=user.status)}**",
            f"**{babax_info[1].format(bot=boy)}**",
            f"**{babax_info[2].format(joined_at_indicator=joined_at_indicator)}**"
        )

        database_info_formatted = (
            f"**{database_info[0].format(prefix=prefix)}**",
            f"**{database_info[1].format(lang=lang)}**"
        )

        if banner and banner.banner:
            other_info_formatted += (f"**{other_info[2].format(banner_url=banner.banner.url)}**",)

        '''view = ProfileMenu(self.bot, inter.author.id)'''

        '''if user.id != inter.author.id:
            view.children = []

            view.bot = self.bot'''

        emb = disnake.Embed(title=f'{profile[0].format(user_name=user.name)}', color=disnake.Color.random())
        emb.add_field(name=f"> {profile[1]}", value='\n'.join(user_info_formatted), inline=False)
        emb.add_field(name=f'> {profile[2]}', value='\n'.join(babax_info_formatted))
        emb.add_field(name=f'> {profile[3]}', value='\n'.join(other_info_formatted))
        emb.add_field(name=f'> {profile[4]}', value='\n'.join(database_info_formatted), inline=False)
        emb.set_author(name=user.name, icon_url=user.avatar)

        if banner and banner.banner:
            emb.set_image(url=banner.banner.url)
        if banner is None:
            return
        
        emb.set_thumbnail(url=user.avatar)
        await inter.reply(embed=emb)

'''class ProfileMenu(ui.View):
    def __init__(self, bot, author_id):
        super().__init__()
        self.timeout = 20
        self.age = None
        self.bot = bot
        self.author_id = author_id
        self.locale = Locale(bot)

    async def interaction_check(self, interaction: disnake.MessageInteraction) -> bool:
        return interaction.user.id == self.author_id
    
    @ui.button(label='Указать возраст', style=disnake.ButtonStyle.green)
    async def set_age(self, button: disnake.ui.Button, inter: disnake.MessageInteraction):
        await inter.response.defer()
        count = await self.locale.get_translation(inter.author.id, 'count')
        errors = await self.locale.get_translation(inter.author.id, 'errors')
        try:
            age_msg = await inter.channel.send(count)

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
                raise commands.CommandError(message=errors[8])
            elif int(age_response.content) > 100:
                await age_msg.delete()
                raise commands.CommandError(message=errors[7])

        except asyncio.TimeoutError:
            await age_msg.delete()
            raise commands.CommandError(message=errors[6])'''

def setup(bot: commands.Bot):
    bot.add_cog(UtilitiesCog(bot))