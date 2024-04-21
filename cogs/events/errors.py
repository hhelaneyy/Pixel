import random
import sqlite3
import disnake
from disnake.ext import commands
from disnake.errors import Forbidden
from datetime import datetime
from core.utilities.embeds import footer

class ErrorsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            em = str(e)
            
            if isinstance(e, commands.CommandNotFound):
                return
            elif isinstance(e, commands.CommandInvokeError):
                E = disnake.Embed(title='❌ Ой-ой, ошибочка вышла!', color=0xb2f557)
                E.add_field(name='Почему вечеринка прервалась?', value=f'```Я ещё не закончила делать уроки...```', inline=False)
                E.add_field(name='Комментарий организатора вечеринки:', value='Эта ошибка возникает в разных случаях. Если вы с ней столкнулись, пожалуйста, сообщите о ней на [официальном сервере разработки Pixel.](https://discord.gg/vmu85FNsqs)')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.owner.avatar)
                await inter.send(embed=E)
                return
            elif isinstance(e, commands.TooManyArguments):
                em = "Слишком много гостей..."
            elif isinstance(e, commands.NotOwner):
                em = "Кажется, вы не организатор вечеринки!"
            elif isinstance(e, commands.UserNotFound):
                em = "Такого гостя нет в моём списке..."
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать эту команду."
            elif isinstance(e, commands.MemberNotFound):
                em = "Такого человека нет в списке гостей вашей вечеринки..."
            elif isinstance(e, commands.MissingRequiredArgument):
                ma = str(e.param).split(":")[0]
                prefix = self.bot.command_prefix
                command_name = inter.invoke_with
                em = f"Отсутствует недостающий аргумент \"{ma}\", пожалуйста, используйте этот вариант: ⟮ {prefix}{command_name} {inter.command.signature} ⟯"
            else:
                em = str(e)

            timestamp = datetime.now()
            m = disnake.Embed(title="❌ Ой-ой, ошибочка вышла!", description=f'Произошла ошибка при использовании команды {inter.data.name}', color=0xff0000)
            m.add_field(name="Почему я вас динамлю?..", value=f"```{em}```")
            m.set_footer(text=f"{random.choice(footer)} ∙ {timestamp.strftime(('%d.%m.%Y, %H:%M'))}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
            d = None
            em = str(e)

            if isinstance(e, commands.CommandInvokeError):
                E = disnake.Embed(title='❌ Ой-ой, ошибочка вышла!', color=0xb2f557)
                E.add_field(name='Почему я вас динамлю?..', value=f'```Я ещё не закончила делать уроки...```', inline=False)
                E.add_field(name='Комментарий организатора вечеринки:', value='Эта ошибка возникает в разных случаях. Если вы с ней столкнулись, пожалуйста, сообщите о ней на [официальном сервере разработки Pixel.](https://discord.gg/vmu85FNsqs)')
                E.set_footer(text=random.choice(footer), icon_url=self.bot.owner.avatar)
                await inter.send(embed=E)
                return
            elif isinstance(e, commands.TooManyArguments):
                em = "Слишком много гостей..."
            elif isinstance(e, commands.NotOwner):
                em = "Кажется, вы не организатор вечеринки!"
            elif isinstance(e, commands.UserNotFound):
                em = "Такого гостя нет в моём списке..."
            elif isinstance(e, commands.MissingPermissions):
                em = "У вас недостаточно прав, чтобы использовать эту команду."
            elif isinstance(e, commands.MemberNotFound):
                em = "Такого человека нет в списке гостей вашей вечеринки..."
            else:
                em = str(e)

            timestamp = datetime.now()
            m = disnake.Embed(title="❌ Ой-ой, ошибочка вышла!", description=f'Произошла ошибка при использовании команды {inter.data.name}', color=0xff0000)
            m.add_field(name="Почему я вас динамлю?..", value=f"```{em}```")
            m.set_footer(text=f"{random.choice(footer)} ∙ {timestamp.strftime(('%d.%m.%Y, %H:%M'))}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorsCog(bot))