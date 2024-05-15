import random
import disnake
from disnake.ext import commands
import sqlite3
from cogs.events.locale import Locale

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

cursor.execute('''
            CREATE TABLE IF NOT EXISTS warns (
            guild_name TEXT,
            user_id TEXT,
            w_count INTEGER
        )
''')
conn.commit()

class ModCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.locale = Locale(bot)

    @commands.slash_command(description='Организатор дал мне право наказывать нарушителей. <3')
    async def moderation(self, inter):
        ...

    @moderation.sub_command(name='ban', description='Мне разрешили банить людей..) / I was allowed to ban people..)')
    @commands.has_permissions(ban_members=True)
    async def ban(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User, reason: str):
        guild = inter.guild

        footer = await self.locale.get_translation(inter.author.id, 'footer')
        ban_translation = await self.locale.get_translation(inter.author.id, "ban")

        await guild.ban(user, reason=reason)
        E = disnake.Embed(title=ban_translation[0], color=0xff0000)
        E.add_field(name=ban_translation[1], value=inter.author.mention)
        E.add_field(name=ban_translation[2], value=user.mention)
        E.add_field(name=ban_translation[3], value=reason)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=user.avatar)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='kick', description='Странный он... Кикну-ка я его. / He is strange... I will kick him.')
    @commands.has_permissions(kick_members=True)
    async def kick(self, inter: disnake.ApplicationCommandInteraction, user: disnake.Member, reason: str):
        guild = inter.guild

        footer = await self.locale.get_translation(inter.author.id, 'footer')
        kick_translation = await self.locale.get_translation(inter.author.id, "kick")

        await guild.kick(user, reason=reason)
        E = disnake.Embed(title=kick_translation[0], color=0xff0000)
        E.add_field(name=kick_translation[1], value=inter.author.mention)
        E.add_field(name=kick_translation[2], value=user.mention)
        E.add_field(name=kick_translation[3], value=reason)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=user.avatar)
        await inter.response.send_message(embed=E)

    async def warn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, reason: str = None):
        cursor.execute('SELECT w_count FROM warns WHERE guild_name = ? AND user_id = ?', (inter.guild.name, member.id))
        row = cursor.fetchone()

        if row:
            count = row[0]
        else:
            count = 0

        count += 1

        if count == 1:
            cursor.execute('INSERT INTO warns (guild_name, user_id, w_count) VALUES (?, ?, ?)', (inter.guild.name, member.id, count))
            conn.commit()
        else:
            cursor.execute('UPDATE warns SET w_count = ? WHERE guild_name = ? AND user_id = ?', (count, inter.guild.name, member.id))
            conn.commit()

        warn_translation = await self.locale.get_translation(inter.author.id, "warn")
        footer = await self.locale.get_translation(inter.author.id, 'footer')

        E = disnake.Embed(title=warn_translation[0], color=0xf4a676)
        E.add_field(name=warn_translation[1], value=inter.author.mention)
        E.add_field(name=warn_translation[2], value=member.mention)
        if reason:
            E.add_field(name=warn_translation[3], value=reason)
        else:
            pass
        E.add_field(name=warn_translation[4], value=count)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='unban', description='Я миротворец. Прощаю всех. / I\'m a peacemaker. I forgive everyone.')
    @commands.has_permissions(ban_members=True)
    async def unban(self, inter: disnake.ApplicationCommandInteraction, user: disnake.User):
        guild = inter.guild
        await guild.unban(user=user)

        unban = await self.locale.get_translation(inter.author.id, 'unban')
        footer = await self.locale.get_translation(inter.author.id, 'footer')

        E = disnake.Embed(title=unban['title'], color=0x94f5c5)
        E.add_field(name='', value=unban['field1'].format(user_mention=user.mention))
        E.set_footer(text=random.choice(footer), icon_url=guild.icon)
        await inter.response.send_message(embed=E)

    @moderation.sub_command(name='unwarn', description='Я прощаю тебя. / I forgive you.')
    @commands.has_permissions(moderate_members=True)
    async def unwarn(self, inter: disnake.ApplicationCommandInteraction, member: disnake.Member, count: int):
        if count <= 0:
            raise commands.CommandError(message=self.locale.get_translation(inter.author.id, "unwarn")[7])
        else:
            cursor.execute('SELECT w_count FROM warns WHERE guild_name = ? AND user_id = ?',
                           (inter.guild.name, member.id))
            row = cursor.fetchone()

            if row:
                warning_count = row[0]
            else:
                warning_count = 0

            if warning_count == 0:
                raise commands.CommandError(message=self.locale.get_translation(inter.author.id, "unwarn")[8])
            if count >= warning_count:
                cursor.execute('DELETE FROM warns WHERE guild_name = ? AND user_id = ?', (inter.guild.name, member.id))
                conn.commit()

                footer = await self.locale.get_translation(inter.author.id, 'footer')
                unwarn = await self.locale.get_translation(inter.author.id, "unwarn")

                embed1 = disnake.Embed(
                    title=unwarn[0],
                    color=0xf8b952
                )
                embed1.add_field(name=unwarn[2], value=inter.author.mention)
                embed1.add_field(name=unwarn[3], value=member.mention)
                embed1.add_field(name=unwarn[4], value=unwarn[6])
                embed1.add_field(name=unwarn[5], value='0')
                embed1.set_footer(text=random.choice(footer), icon_url=inter.author.avatar)
                await inter.response.send_message(embed=embed1)
            else:
                warning_count -= count
                cursor.execute('UPDATE warns SET w_count = ? WHERE guild_name = ? AND user_id = ?',
                               (warning_count, inter.guild.name, member.id))
                conn.commit()

                embed = disnake.Embed(
                    title=unwarn[1],
                    color=0xf8b952
                )
                embed.add_field(name=unwarn[2],
                                value=inter.author.mention)
                embed.add_field(name=unwarn[3], value=member.mention)
                embed.add_field(name=unwarn[4], value=count)
                embed.add_field(name=unwarn[5], value=warning_count)
                embed.set_footer(text=random.choice(footer), icon_url=inter.author.avatar)
                await inter.response.send_message(embed=embed)

    @moderation.sub_command(name='lockdown', description='Блокируйте все чаты ради безопасности! / Lock all chats for security!')
    @commands.has_permissions(administrator=True)
    async def lock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        footer = await self.locale.get_translation(inter.author.id, 'footer')
        lockdown = await self.locale.get_translation(inter.author.id, "lockdown")
        errors = await self.locale.get_translation(inter.author.id, 'errors')

        guild = inter.guild
        channels = await guild.fetch_channels()

        cursor.execute('SELECT role_id FROM lkroles WHERE guild_id = ?', (guild.id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise commands.CommandError(message=errors['deny_role'])
        else:
            role = guild.get_role(role_id[0])
        if role:
            for channel in channels:
                await channel.set_permissions(role, send_messages=False)

            E = disnake.Embed(title=lockdown[2], color=0xff0000)
            E.add_field(name=lockdown[3], value=f'```{lockdown[4].format(role.name)}```')
            E.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await inter.followup.send(embed=E)
        else:
            raise commands.CommandError(message=errors['deny_role'])

    @moderation.sub_command(name='unlock', description='Разблокируйте все чаты ради безопасности! / Unlock all chats for safety!')
    @commands.has_permissions(administrator=True)
    async def unlock(self, inter: disnake.ApplicationCommandInteraction):
        await inter.response.defer()
        footer = await self.locale.get_translation(inter.author.id, 'footer')
        errors = await self.locale.get_translation(inter.author.id, 'errors')
        unlock = await self.locale.get_translation(inter.author.id, "unlock")

        guild = inter.guild
        channels = await guild.fetch_channels()

        cursor.execute('SELECT role_id FROM lkroles WHERE guild_id = ?', (guild.id,))
        role_id = cursor.fetchone()

        if role_id is None:
            raise commands.CommandError(message=errors['allow_role'])
        else:
            role = guild.get_role(role_id[0])
        if role:
            for channel in channels:
                await channel.set_permissions(role, send_messages=None)

            E = disnake.Embed(title=unlock[2], color=0x8eff77)
            E.add_field(name=unlock[3], value=f'```{unlock[4].format(role.name)}```')
            E.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await inter.followup.send(embed=E)
        else:
            raise commands.CommandError(message=errors['allow_role'])

    @moderation.sub_command(name='clear', description='Помогу вынести мусор! / Let me help you take out the trash!')
    @commands.has_permissions(manage_messages=True)
    async def clear(self, inter: disnake.ApplicationCommandInteraction, amount: int):
        footer = await self.locale.get_translation(inter.author.id, 'footer')
        errors = await self.locale.get_translation(inter.author.id, 'errors')
        clear = await self.locale.get_translation(inter.author.id, "clear")
        if amount <= 0:
            raise commands.CommandError(message=errors['negative_number'])
        
        elif amount >= 75:
            raise commands.CommandError(message=errors['bigger_75'])

        messages = await inter.channel.history(limit=amount).flatten()
        messages = [msg for msg in messages if msg.id != inter.id]
        await inter.channel.delete_messages(messages)

        embed = disnake.Embed(title=clear[0], description=clear[1].format(amount=amount), color=0x50c878)
        author = inter.author
        embed.set_footer(text=random.choice(footer), icon_url=author.avatar.url)
        await inter.response.send_message(embed=embed, ephemeral=True)

def setup(bot: commands.Bot):
    bot.add_cog(ModCog(bot))