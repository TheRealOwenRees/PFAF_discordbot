import os
import logging

from dotenv import load_dotenv

from discord import Game, Intents
from discord.ext.commands import Bot

from cogs.pfaf_slash import PfafSlashCommands
from cogs.bot_info import BotInfo

load_dotenv()
DISCORD_TOKEN = os.getenv('DISCORD_TOKEN')

# logging.basicConfig(level=logging.DEBUG)
# logger = logging.getLogger('discord')
# logger.setLevel(logging.CRITICAL)
# handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')
# handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
# logger.addHandler(handler)

intents = Intents.default()
intents.message_content = True

bot = Bot(
    debug_guilds=[1002507312159797318], # remove after testing
    case_insensitive=True,
    intents=intents,
    help_command=None,
    activity=Game(name=f'/help')
)
bot.add_cog(PfafSlashCommands(bot))
bot.add_cog(BotInfo(bot))

@bot.event
async def on_ready():
    print(f'{bot.user} has connected to Discord!')

bot.run(DISCORD_TOKEN)
