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
            raise commands.CommandError(message='Место полложение хостинга не удовлетворяет условиям использования OpenAI.')
        
def setup(bot: commands.Bot):
    bot.add_cog(OpenaiCog(bot))