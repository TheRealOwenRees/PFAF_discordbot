import os
from datetime import datetime

import discord
from discord.ext.commands import Cog, slash_command


class BotInfo(Cog):
    def __init__(self, bot):
        self.bot = bot
        self.start_time = datetime.now()

    @slash_command(name='help', description='show help')
    async def help(self, ctx: discord.ApplicationContext):
        embed = discord.Embed(
            title='PFAF Bot Help',
            description='PFAF Bot pulls data from PFAF.org',
            colour=0x41c03f
        ).add_field(
            name=f'`/search`',
            value='Searches for plants in the PFAF database by common names (english), returning latin names',
            inline=True
        ).add_field(
            name=f'`/details`',
            value='Returns details of the plant. Requires a latin name as input. A second optional argument (verbose) returns much more detail.',
            inline=True
        ).add_field(
            name=f'`/stats`',
            value='PFAF Bot stats',
            inline=True
        ).add_field(
            name=f'`/invite`',
            value='Bot invite link',
            inline=True
        ).add_field(
            name=f'`/source`',
            value='Links to the bot\'s GitHub repo',
            inline=True
        ).add_field(
            name=f'`/help`',
            value='Shows this message',
            inline=True
        )
        await ctx.respond(embed=embed)

    @slash_command(name='invite', description='display an invite link for this bot')
    async def invite(self, ctx: discord.ApplicationContext):
        await ctx.respond('no invite link set up')

    @slash_command(name='source', description='display the url to this bot\'s Github repo')
    async def source(self, ctx: discord.ApplicationContext):
        await ctx.respond('no Gihub link set up')  

    @slash_command(name='stats', description='display bot stats')
    async def stats(self, ctx: discord.ApplicationContext):
        info = await self.bot.application_info()
        embed = discord.Embed(
            title=f'{info.name}',
            description=f'{info.description}',
            colour=0x1aaae5,
        ).add_field(
            name='Guild Count',
            value=len(self.bot.guilds),
            inline=True
        ).add_field(
            name='User Count',
            value=len(self.bot.users),
            inline=True
        ).add_field(
            name='Uptime',
            value=f'{datetime.now() - self.start_time}',
            inline=True
        ).add_field(
            name='Latency',
            value=f'{round(self.bot.latency * 1000, 2)}ms',
            inline=True
        )
        # .set_footer(text=f'Made by {info.owner}', icon_url=info.owner.avatar_url)
        await ctx.respond(embed=embed)