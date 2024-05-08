import sqlite3
import disnake
from disnake.ext import commands
import openai

class OpenaiCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    '''@commands.slash_command(name="write", description="Задайте вопрос нейросети при помощи «GPT-3.5-Turbo».")
    async def write(self, inter: disnake.ApplicationCommandInteraction, *, model: str = commands.Param(choices=['Kandinsky', 'ChatGPT 3.5 Turbo']), prompt):
        author = inter.author

        await inter.response.defer()
        if model == 'ChatGPT 3.5 Turbo':
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
                raise commands.CommandError(message='Невозможно сгенерировать ответ. Обратитесь к главному разработчику для выяснения проблемы.')

        elif model == 'Kandinsky':
            api = Text2ImageAPI('https://api-key.fusionbrain.ai/', '5963231F10FA2F5C48AFBD67FEE5440F', '2C2A0E9EB941E04B0DA386978042DB94')
            model_id = api.get_model()
            uuid = api.generate("Sun in sky", model_id)
            images = api.check_generation(uuid)
            print(images)'''

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',
            'X-Secret': f'Secret {secret_key}',
        }

    def get_model(self):
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()
        return data[0]['id']

    def generate(self, prompt, model, images=1, width=1024, height=1024):
        params = {
            "type": "GENERATE",
            "numImages": images,
            "width": width,
            "height": height,
            "generateParams": {
                "query": f"{prompt}"
            }
        }

        data = {
            'model_id': (None, model),
            'params': (None, json.dumps(params), 'application/json')
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)
        
def setup(bot: commands.Bot):
    bot.add_cog(OpenaiCog(bot))