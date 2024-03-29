import random
import disnake
from disnake.ext import commands
from core.utilities.embeds import footer

class ModCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(description='Организатор дал мне право наказывать нарушителей. <3')
    async def moderation(self, inter):
        ...

    @moderation.sub_command(name='clear', description='Как много мусора... Но я могу очистить его!')
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