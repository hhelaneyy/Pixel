import asyncio
import sys
import disnake
from disnake.ext import commands
import openai
import json
import os
import time
import sqlite3

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

with open('config.json') as f:
    data = json.load(f)
    token = data["token"]
    openai.api_key = data['gpt_token']

intents = disnake.Intents.all()
bot = commands.Bot(command_prefix=None, help_command=None, intents=intents)

@bot.event
async def on_message(message: disnake.Message):
    default_prefix = 'px-'
    cursor.execute('SELECT prefix_name FROM prefix WHERE user_id = ?', (message.author.id, ))
    prefix = cursor.fetchone()

    if prefix:
        bot.command_prefix = prefix[0]
    else:
        bot.command_prefix = default_prefix

        cursor.execute('INSERT OR IGNORE INTO prefix (user_id, prefix_name) VALUES (?, ?)', (message.author.id, default_prefix))
        conn.commit()

    await bot.process_commands(message)

@bot.event
async def on_ready():
    bot.start_time = time.time()
    print("Ваш виртуальный ассистент запущен.")
    for root, dirs, files in os.walk('cogs'):
        for dir in dirs:
            for filename in os.listdir(os.path.join('cogs', dir)):
                if filename.endswith('.py'):
                    bot.load_extension(f'cogs.{dir}.{filename[:-3]}')

@bot.command(description="Мейсон спать.")
async def restart(ctx):
    if ctx.author.id == bot.owner.id:
        await ctx.reply("⭐ Трансляция не умерла... но сейчас, это конец её вещания.")
        await asyncio.sleep(1)

        python = sys.executable
        os.execl(python, python, *sys.argv)

bot.run(token)