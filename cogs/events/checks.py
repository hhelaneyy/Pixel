import sqlite3
from disnake.ext import commands

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

def is_blacklisted(ctx):
    cursor.execute("SELECT blacklisted FROM blacklist WHERE user_id = ?", (ctx.author.id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        msg = 'User is blacklisted'
        raise commands.CheckFailure(msg)
    return True

def is_blacklisted_app(interaction):
    cursor.execute("SELECT blacklisted FROM blacklist WHERE user_id = ?", (interaction.author.id,))
    result = cursor.fetchone()

    if result and result[0] == 1:
        msg = 'User is blacklisted'
        raise commands.CheckFailure(msg)
    return True

def setup(bot: commands.Bot):   
    bot.add_check(is_blacklisted, call_once=False)
    bot.add_app_command_check(is_blacklisted_app, call_once=False, slash_commands=True)