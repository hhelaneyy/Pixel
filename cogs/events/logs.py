from datetime import datetime
import random
import disnake
from disnake.ext import commands
import sqlite3
from core.utilities.embeds import footer

conn = sqlite3.connect('Pixel.db')
cursor = conn.cursor()

class LogsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot

    def get_log_channel(self, guild):
        connection = sqlite3.connect('Pixel.db')
        cursor = connection.cursor()
        cursor.execute('SELECT channel_id FROM logs WHERE guild_id=?', (str(guild.id),))
        result = cursor.fetchone()
        if result:
            channel_id = result[0]
            return guild.get_channel(channel_id)
        return None
        
    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            if before.author.bot or before.webhook_id:
                return

            if before.content == after.content:
                return
            else:
                embed = disnake.Embed(title="🔖 Изменение сообщения.", color=0xfaee77)
                embed.add_field(name="Автор:", value=f'{before.author.mention}')
                embed.add_field(name="Канал:", value=f'{before.channel.mention}')
                embed.add_field(name="Перейти к сообщению", value=f'[Сообщение]({after.jump_url})')
                embed.add_field(name="Первоначальное сообщение:", value=f'```{before.content}```', inline=False)
                embed.add_field(name="Изменено на:", value=f'```{after.content}```', inline=False)
                embed.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await log_channel.send(embed=embed)
        else:
            return

    @commands.Cog.listener()
    async def on_message_delete(self, before):
        log_channel = self.get_log_channel(before.guild)
        if log_channel:
            if before.author.bot or before.webhook_id:
                return
            else:
                embed = disnake.Embed(title="🛑 Удаление сообщения.", color=0xec9d4f)
                embed.add_field(name="Автор:", value=f'{before.author.mention}')
                embed.add_field(name="Канал:", value=f'{before.channel.mention}')
                embed.add_field(name='Контент сообщения:', value=before.content, inline=False)
                embed.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
                await log_channel.send(embed=embed)
        else:
            return
        
    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        log_channel = self.get_log_channel(member.guild)
        guild_id = member.guild.id
        guild = member.guild
        created_at_indicator = f'<t:{int(member.created_at.timestamp())}:F>'

        if log_channel:
            babax = await self.bot.fetch_user(member.id)

            cursor.execute('SELECT role_id FROM auto_roles WHERE guild_id = ?', (guild_id,))
            role_id = cursor.fetchone()

            if role_id:
                role = member.guild.get_role(role_id[0])
                if role:
                    await member.add_roles(role)

            embed = disnake.Embed(title="👤 Новый гость на вечеринке!", color=0x8bcdfe)
            embed.add_field(name="Никнейм участник:", value=f'{member.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=member.avatar)

            if babax.banner:
                embed.set_image(url=babax.banner.url)
            else:
                pass

            embed.set_footer(text=random.choice(footer), icon_url=member.guild.icon)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member: disnake.Member):
        log_channel = self.get_log_channel(member.guild)
        created_at_indicator = f'<t:{int(member.created_at.timestamp())}:F>'
        if log_channel:
            babax = await self.bot.fetch_user(member.id)

            embed = disnake.Embed(title="👤 Гость покинул вечеринку...", color=0x608daf)
            embed.add_field(name="Никнейм участник:", value=f'{member.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=member.avatar)

            if babax.banner:
                embed.set_image(url=babax.banner.url)
            else:
                pass

            embed.set_footer(text=random.choice(footer), icon_url=member.guild.icon)

            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild: disnake.Guild, user: disnake.User):
        log_channel = self.get_log_channel(guild)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="🔴 Гость заблокирован.", color=0xd54e4e)
            embed.add_field(name="Никнейм участник:", value=f'{user.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.add_field(name='Причина:', value='???')
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_unban(self, guild: disnake.Guild, user: disnake.User):
        log_channel = self.get_log_channel(guild)
        created_at_indicator = f'<t:{int(user.created_at.timestamp())}:F>'
        if log_channel:
            embed = disnake.Embed(title="🟢 Гость разблокирован.", color=0x90fd6a)
            embed.add_field(name="Никнейм участник:", value=f'{user.mention}')
            embed.add_field(name='Дата регистрации:', value=created_at_indicator)
            embed.set_thumbnail(url=user.avatar)
            embed.set_footer(text=random.choice(footer), icon_url=guild.icon)
            await log_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite: disnake.Invite):
        channel = await self.bot.fetch_channel(1211298019866054678)
        guild = invite.guild

        E = disnake.Embed(title='🌌 Создано новое приглашение на вечеринку!', color=0xdaa5ff)
        E.add_field(name='Новое приглашение:', value=invite.url)
        E.set_footer(text=random.choice(footer), icon_url=self.bot.user.avatar)
        E.set_thumbnail(url=guild.icon)
        await channel.send(embed=E)

def setup(bot: commands.Bot):
    bot.add_cog(LogsCog(bot))