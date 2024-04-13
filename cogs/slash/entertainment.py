import disnake
from disnake.ext import commands
import random
import requests
from core.utilities.embeds import footer

TENOR_API_KEY = 'AIzaSyDIzri_pLPwTV_49BI3sDGcgJPSQ6DD3-g'

class EntertainmentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.proposals = {}

    @commands.slash_command(description='Веселью нет конца!')
    async def entertainment(self, inter):
        ...

    @entertainment.sub_command(name='roleplay', description="Вырази свои чувства!")
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, action: str = commands.Param(choices=["Hug / Обнять", "Kiss / Поцеловать", 'Feed / Накормить', "Pat / Погладить", "Slap / Пощёчина", 'Poke / Потыкать', "Punch / Ударить", "Bite / Укусить"], description='Выбор действия над участником.'), ping: str = commands.Param(choices=['Да', 'Нет'], description='Упомянуть участника или нет.')):
        author = inter.author
        nsfw_actions = ["Suck / Отсосать", 'Rape / Изнасиловать']

        if action == nsfw_actions and not inter.channel.nsfw():
            E = disnake.Embed(title='⚠️ Произошла ошибка.', description='Публике нельзя на такое смотреть.', color=disnake.Color.yellow())
            E.add_field(name='Что же не так?', value=f'```Данное действие запрещено использовать в чатах, где происходит основное общение.')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E, ephemeral=True)
            return

        if action == 'Feed / Накормить':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_feed&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")
        elif action == 'Poke / Потыкать':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_poke&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")     
        elif action == 'Bite / Укусить':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_bite&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")  
        elif action == 'Punch / Ударить':
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_punch&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")  
        else:
            response = requests.get(f"https://tenor.googleapis.com/v2/search?q=anime_{action}&key={TENOR_API_KEY}&media_filter=gif&limit=1&random=True")
        if response.status_code == 200:
            data = response.json()
            gif_url = data['results'][0]['media_formats']['gif']['url']
        else:
            raise commands.CommandError(message='Произошла ошибка при поиске гиф изображения.')
        
        if user.id == author.id:
            raise commands.CommandError(message='Вы не можете выразить свои чувства на самом себе. Вы же не самовлюблённый...')

        if action == "Hug / Обнять":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed=emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} обнял(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed=emb2)

        elif action == 'Feed / Накормить':
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == 'Poke / Потыкать':
            if author.id == self.bot.owner.id:
                if ping == 'Нет':
                    emb2 = disnake.Embed(title=f"**{author.name} потыкал(а) {user.name}**", color=disnake.Color.random())
                    emb2.set_image(url=gif_url)
                    emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                    await inter.send(embed = emb2)
                else:
                    emb2 = disnake.Embed(title=f"**{author.name} потыкал(а) {user.name}**", color=disnake.Color.random())
                    emb2.set_image(url=gif_url)
                    emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                    await inter.send(user.mention, embed = emb2)
            else:
                E = disnake.Embed(title='⚠️ Произошла ошибка', description='Проблемы с выполнением действия над пользователем.', color=disnake.Color.yellow())
                E.add_field(name='Что же не так?', value=f'```Прошу прощения, но данное действие ещё не доступно для пользователей бота. Идёт бета-тестирование действия. Разработчик сообщит на официальном сервере разработки как только действие станет доступно.```')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await inter.response.send_message(embed=E, ephemeral=True)

        elif action == "Kiss / Поцеловать":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} поцеловал(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Pat / Погладить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} погладил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Slap / Пощёчина":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} дал(а) пощёчину {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Punch / Ударить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} ударил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Bite / Укусить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} укусил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Feed / Накормить":
            if ping == 'Нет':
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} накормил(а) {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)
            
    @entertainment.sub_command(name='design', description="Хотите взглянуть на оформление своего профиля?")
    async def decor(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        if user is None:
            user = inter.author

        banner = await self.bot.fetch_user(user.id)
        bann = f' | [Скачать баннер]({banner.banner})'
        ava = f'[Скачать аватар]({user.display_avatar.url})'
        warn = '[ Аватарка находится справа сверху, а баннер снизу на весь Embed. ]'

        E = disnake.Embed(description=f'{ava if user.avatar else ""}{bann if banner.banner else ""} \n\n{warn if banner.banner else ""}', color=disnake.Color.random())
        E.set_author(name=user.name, icon_url=user.display_avatar)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)

        if user.avatar and banner.banner != None:
            E.set_thumbnail(url=user.display_avatar)
        else:
            E.set_image(url=user.display_avatar)

        if banner and banner.banner:
            E.set_image(url=banner.banner.url)
        if banner is None:
            pass

        await inter.send(embed=E)

    @entertainment.sub_command(name='coinflip', description='Ну что, подбросим?')
    async def coin(self, inter: disnake.ApplicationCommandInteraction, side: str = commands.Param(choices=['Орёл', 'Решка'])):
        sd = ['Орёл', 'Решка']
        result = ['Орёл', 'Решка']
        rst = random.choice(result)
        bot_side = random.choice(sd)

        if bot_side == rst and side == rst:
            E = disnake.Embed(title='💜 Монетка подброшена!', color=0xfff977)
            E.add_field(name='Результат подбрасывания:', value=f'```Ого, а ты везунчик! Выпал: {rst}, твой выбор - {side}, мой выбор - {bot_side}. У нас ничья. <3```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
        elif bot_side == rst and side != rst:
            E = disnake.Embed(title='💜 Монетка подброшена!', color=0xfff977)
            E.add_field(name='Результат подбрасывания:', value=f'```Ха-ха, ты проиграл! Выпал: {rst}, твой выбор - {side}, мой выбор - {bot_side}. Моя правда. <3```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)
        else:
            E = disnake.Embed(title='💜 Монетка подброшена!', color=0xfff977)
            E.add_field(name='Результат подбрасывания:', value=f'```Чёрт, ты выиграл... Выпал: {rst}, твой выбор - {side}, мой выбор - {bot_side}. Была не права, извиняюсь. <3```')
            E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
            await inter.response.send_message(embed=E)

def setup(bot: commands.Bot):
    bot.add_cog(EntertainmentCog(bot))