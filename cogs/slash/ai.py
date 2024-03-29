import sqlite3
import disnake
from disnake.ext import commands
import openai

class OpenaiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    @commands.slash_command(name="write", description="Задайте вопрос нейросети при помощи «GPT-3.5-Turbo».")
    async def write(self, inter: disnake.ApplicationCommandInteraction, *, prompt):
        author = inter.author

        await inter.response.defer()

        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo-0613",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": prompt}
                ],
            )
            reply = response.choices[0].message.content
            embed = disnake.Embed(title=f"⟩ Ответ нейросети:", description=reply, color=disnake.Color.blurple())
            embed.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
            await inter.followup.send(embed=embed)

        except Exception as e:
            m1 = disnake.Embed(title="⚠️ Произошла ошибка.", description="Ваше местоположение...", color=0xff6969)
            m1.add_field(name="Что же не так?", value=f"```Ваше местоположение не удовлетворяет условиям пользования технологией OpenAI.```")
            m1.set_footer(text=f"Поддерживается благодаря {self.bot.owner.name}", icon_url=self.bot.owner.avatar.url)
            await inter.followup.send(embed=m1, ephemeral=True)
            return
        
def setup(bot: commands.Bot):
    bot.add_cog(OpenaiCog(bot))