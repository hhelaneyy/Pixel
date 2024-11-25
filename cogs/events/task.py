import asyncio
import random
import sqlite3
import disnake
from disnake.ext import commands, tasks

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
         CREATE TABLE IF NOT EXISTS autothread (
               id INTEGER PRIMARY KEY,
               guild_id INTEGER NOT NULL,
               guild_name TEXT,
               channel_id INTEGER NOT NULL
)
''')
conn.commit()

cursor.execute('''
               CREATE TABLE IF NOT EXISTS atembed (
               id INTEGER PRIMARY KEY,
               guild_id INTEGER NOT NULL,
               guild_name TEXT,
               channel_id INTEGER NOT NULL,
               name TEXT,
               title TEXT,
               description TEXT,
               color INTEGER
)
''')
conn.commit()

class EventsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.status.start()

    @tasks.loop(seconds=1)
    async def status(self):
        users = []
        for guild in self.bot.guilds:
            users.extend(guild.members)

        if users:
            rdu = random.choice(users)
            rduu = rdu.name

        await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(name=f'at {rduu}', type=disnake.ActivityType.watching))
        await asyncio.sleep(25)
        await self.bot.change_presence(status=disnake.Status.online, activity=disnake.Activity(name=f'7 guides to start a Party', url='https://www.youtube.com/watch?v=ysFsS7ReTNc', type=disnake.ActivityType.streaming))
        await asyncio.sleep(300)

    @status.before_loop
    async def before_status(self):
        await self.bot.wait_until_ready()

    def cog_unload(self):
        self.status.cancel()

    def get_channels(self, guild: disnake.Guild):
        cursor.execute('SELECT channel_id FROM autothread WHERE guild_id=?', (str(guild.id),))
        results = cursor.fetchall()
        channels = []
        for result in results:
            channel_id = result[0]
            channel = guild.get_channel(channel_id)
            if channel:
                channels.append(channel)
        return channels

    @commands.Cog.listener()
    async def on_voice_state_update(self, member: disnake.Member, before, after):
        cursor.execute('SELECT channel_id FROM voices WHERE guild_id = ?', (member.guild.id,))
        channel_id = cursor.fetchone()

        if after.channel:
            if channel_id:
                channel = await self.bot.fetch_channel(channel_id[0])
                if after.channel.id != channel.id:
                    return
            else:
                return
        else:
            user_chan_id = cursor.execute('SELECT channel_id FROM user_voices WHERE guild_id = ? AND user_id = ?', (member.guild.id, member.id)).fetchone()
            if user_chan_id:
                user_chan = await self.bot.fetch_channel(user_chan_id[0])
                if user_chan:
                    cursor.execute('DELETE FROM user_voices WHERE channel_id = ?', (user_chan.id,))
                    conn.commit()
                    await user_chan.delete()

        user_chan = None

        if after.channel:
            if after.channel.name == member.name and after.channel.category == channel.category:
                user_chan = after.channel
            else:
                user_chan = await member.guild.create_voice_channel(name=member.name, user_limit=1, category=channel.category)
                cursor.execute('INSERT INTO user_voices (guild_id, user_id, channel_id) VALUES (?, ?, ?)', (member.guild.id, member.id, user_chan.id))
                conn.commit()

                await member.move_to(user_chan)
                await user_chan.set_permissions(member, manage_channels=True, connect=True)

    @commands.Cog.listener()
    async def on_message(self, message: disnake.Message):
        guild_id = message.guild.id
        user = message.author
        channels = self.get_channels(message.guild)

        for channel in channels:
            if message.author == self.bot.user or message.channel != channel:
                continue

            cursor.execute('SELECT name, title, description, color FROM atembed WHERE guild_id = ? AND channel_id = ?', (guild_id, channel.id))
            embed_data = cursor.fetchone()

            if embed_data:
                name, title, description, color = embed_data
                if '{user.name}' in name:
                    name = name.format(user=user)
            else:
                name = f'Обсуждение тематики {user.name}'
                title = 'Эта ветка была создана автоматически'
                description = f'Здесь вы спокойно можете обсудить заданную автором сообщения тематику. Перед дискуссией просим ознакомиться с правилами: {message.guild.rules_channel.mention if message.guild.rules_channel else "Канал с правилами не установлен"}.'
                color = 0x8eaaf5

            if isinstance(color, str) and color.startswith('0x'):
                color = int(color, 16)

            embed = disnake.Embed(title=title, description=description, color=color)

            babax = await channel.create_thread(name=name, auto_archive_duration=None, message=message)
            await babax.send(embed=embed)

def setup(bot: commands.Bot):
    bot.add_cog(EventsCog(bot))