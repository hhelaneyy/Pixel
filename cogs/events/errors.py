import random
import sqlite3
import disnake
from disnake.ext import commands
from disnake.errors import Forbidden
from datetime import datetime
from cogs.events.locale import Locale

class ErrorsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.locale = Locale(bot)

    @commands.Cog.listener()
    async def on_slash_command_error(self, inter: disnake.ApplicationCommandInteraction, e):
        d = None
        em = str(e)

        errors = await self.locale.get_translation(inter.author.id, 'errors')
        footer = await self.locale.get_translation(inter.author.id, 'footer')
        embed = errors['embed']

        channel = self.bot.get_channel(1235610149763420292)

        if channel:
            E = disnake.Embed(title='🚨 Произошла непредвиденная ошибка!', description=f'Произошла ошибка при использовании команды {inter.data.name}', color=0xff0000)
            E.add_field(name='Описание ошибки:', value=f'```{em}```')
            await channel.send(embed=E)

        if isinstance(e, commands.CommandInvokeError):
            E = disnake.Embed(title=embed['title'], color=0xb2f557)
            E.add_field(name=embed['error_desc'], value=f'```{embed['value']}```', inline=False)
            E.add_field(name=embed['field1'], value=embed['field2'])
            E.set_footer(text=random.choice(footer), icon_url=self.bot.owner.avatar)
            await inter.send(embed=E)
            return
        elif isinstance(e, commands.TooManyArguments):
            em = errors['many_guets']
        elif isinstance(e, commands.NotOwner):
            em = errors['not_organizer']
        elif isinstance(e, commands.UserNotFound):
            em = errors['user_notfound']
        elif isinstance(e, commands.MissingPermissions):
            em = errors['miss_perms']
        elif isinstance(e, commands.MemberNotFound):
            em = errors['member_notfound']
        else:
            em = str(e)

            timestamp = datetime.now()
            m = disnake.Embed(title=embed['title'], description=f'{embed['description']} {inter.data.name}', color=0xff0000)
            m.add_field(name=embed['error_desc'], value=f"```{em}```")
            m.set_footer(text=f"{random.choice(footer)} ∙ {timestamp.strftime(('%d.%m.%Y, %H:%M'))}", icon_url=self.bot.user.avatar.url)
            await inter.send(embed=m, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ErrorsCog(bot))