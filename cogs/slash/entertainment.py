import disnake
from disnake.ext import commands
import random
import requests
from core.utilities.embeds import NSFW
from cogs.events.locale import Locale

class EntertainmentCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.proposals = {}
        self.locale = Locale(bot)

    @commands.slash_command(description='Веселью нет конца!')
    async def entertainment(self, inter):
        ...

    @entertainment.sub_command(name='roleplay', description="Вырази свои чувства! / Express your feelings!")
    async def rp(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, action: str = commands.Param(choices=["Hug / Обнять", "Kiss / Поцеловать", 'Feed / Накормить', "Pat / Погладить", "Slap / Пощёчина", 'Poke / Потыкать', "Punch / Ударить", "Bite / Укусить", 'Rape / Изнасиловать', 'Suck / Отсосать'], description='Выбор действия над участником.'), ping: str = commands.Param(choices=['Yes / Да', 'No / Нет'], description='Упомянуть участника или нет.')):
        author = inter.author
        msg = await self.locale.get_translation(author.id, 'errors')
        nsfw_actions = ["Suck / Отсосать", 'Rape / Изнасиловать']

        if action == nsfw_actions and not inter.channel.nsfw():
            raise commands.CommandError(message=msg[0])

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

        actions = await self.locale.get_translation(author.id, 'actions')
        footer = await self.locale.get_translation(author.id, 'footer')

        if action == "Hug / Обнять":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[0]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed=emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[0]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed=emb2)

        elif action == 'Feed / Накормить':
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[3]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[3]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == 'Poke / Потыкать':
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[6]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[6]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Kiss / Поцеловать":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[1]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[1]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Pat / Погладить":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[4]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[4]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Slap / Пощёчина":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[2]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[2]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Punch / Ударить":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[5]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[5]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == "Bite / Укусить":
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[7]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[7]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=gif_url)
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == 'Rape / Изнасиловать':
            if ping == 'No / Нет':
                emb2 = disnake.Embed(title=f"**{author.name} {actions[5]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=random.choice(NSFW))
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(embed = emb2)
            else:
                emb2 = disnake.Embed(title=f"**{author.name} {actions[5]} {user.name}**", color=disnake.Color.random())
                emb2.set_image(url=random.choice(NSFW))
                emb2.set_footer(text=random.choice(footer), icon_url=author.avatar)
                await inter.send(user.mention, embed = emb2)

        elif action == 'Suck / Отсосать':
            raise commands.CommandError(message=msg[1])
            
    @entertainment.sub_command(name='design', description="Ваш профиль прекрасен! / Your profile is wonderful!")
    async def decor(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User = None):
        if user is None:
            user = inter.author

        decor = await self.locale.get_translation(inter.author.id, "decor")
        footer = await self.locale.get_translation(inter.author.id, 'footer')

        banner = await self.bot.fetch_user(user.id)
        bann = f'[{decor[0]}]({banner.banner.url})' if banner.banner else ""
        ava = f'[{decor[1]}]({user.display_avatar.url})' if user.avatar else ""
        warn = f'{decor[2]}' if banner.banner else ""

        E = disnake.Embed(description=f'{ava} | {bann} \n\n{warn}', color=disnake.Color.random())
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

        await inter.response.send_message(embed=E)

    @entertainment.sub_command(name='coinflip', description='Ну что, подбросим? / Well, shall we flip?')
    async def coin(self, inter: disnake.ApplicationCommandInteraction, side: str = commands.Param(choices=['Heads / Орёл', 'Tails / Решка'])):
        sd = ['Heads / Орёл', 'Tails / Решка']
        result = ['Heads / Орёл', 'Tails / Решка']
        rst = random.choice(result)
        bot_side = random.choice(sd)

        coinflip_results = await self.locale.get_translation(inter.author.id, "coinflip_results")

        if bot_side == rst and side == rst:
            message = coinflip_results["win"].format(rst=rst, side=side, bot_side=bot_side)
        elif bot_side == rst and side != rst:
            message = coinflip_results["lose"].format(rst=rst, side=side, bot_side=bot_side)
        else:
            message = coinflip_results["draw"].format(rst=rst, side=side, bot_side=bot_side)

        footer = await self.locale.get_translation(inter.author.id, 'footer')
        coinflip_title = await self.locale.get_translation(inter.author.id, "coinflip_title")
        coinflip_results_title = await self.locale.get_translation(inter.author.id, "coinflip_results")

        E = disnake.Embed(title=coinflip_title, color=0xfff977)
        E.add_field(name=coinflip_results_title["title"], value=f'```{message}```')
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=E)

def setup(bot: commands.Bot):
    bot.add_cog(EntertainmentCog(bot))
