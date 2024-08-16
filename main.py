import logging
import os
import sys
import threading

import discord
from colorama import Fore, Style
from discord.ext import commands

# Enviroment Settings
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='*@#RH@(*U$YH*&HF@U#H', intents=intents)
logging.basicConfig(level=logging.INFO,
  format='\033[1m %(asctime)s %(levelname)s \033[0m    %(message)s', 
  datefmt=Fore.LIGHTBLACK_EX+'%Y-%m-%d %H:%M:%S'+Fore.RESET)  
logging.info(Fore.BLUE + f"Xyrdron Pty Ltd\nMikuBOT")
logging.info(Fore.BLUE+'Connecting to Discord')

# Bot Startup
@bot.event
async def on_ready():
    logging.info(Fore.GREEN+'Connected to Discord')

    # Cogs
    logging.info(Fore.BLUE+'Loading commands')
    for filename in os.listdir('cogs'):
        if filename.endswith(".py"):
            cog_name = filename[:-3]
            cog_module = f"cogs.{cog_name}"

            try:
                if cog_name not in bot.cogs:
                    logging.info(Fore.BLUE+'Loading '+cog_module)
                    if cog_name == 'example-cog':
                        logging.info(Fore.YELLOW+f'Skipped {cog_name}')
                    else:
                        await bot.load_extension(cog_module)
                    logging.info(Fore.GREEN+'Loaded ' + cog_module)
            except Exception as e:
                logging.critical(Fore.RED+f'Failed to load {cog_module} {e}')
                logging.critical(Fore.RED+'Failed to complete boot sequence due to exception')
                sys.exit('Failed to complete boot sequence due to exception')
    logging.info(Fore.GREEN+'Loaded all commands')


    # Syncing
    try:
        logging.info(Fore.BLUE+'Syncing command tree')
        await bot.wait_until_ready()
        await bot.tree.sync()
        logging.info(Fore.GREEN+'Commands synced')
    except Exception as e:
        logging.critical(Fore.RED+f'Failed to sync command tree {e}')
        logging.critical(Fore.RED+'Failed to complete boot sequence due to exception')
        sys.exit('Failed to complete boot sequence due to exception')

    # Presence
    try:
        logging.info(Fore.BLUE+'Setting presence')
        await bot.change_presence(activity=discord.Game(name="giving u a tickle :D"))
        logging.info(Fore.GREEN+'Presence set')
    except Exception as e:
        logging.critical(Fore.RED+f'Failed to set presence {e}')
        logging.critical(Fore.RED+'Failed to complete boot sequence due to exception')
        sys.exit('Failed to complete boot sequence due to exception')

    # Miku is booted!1!1!1
    logging.info(Fore.GREEN+f'Boot successful, Logged in as {bot.user}')

def run():
    # IMPORTANT
    # TO ALL CONTRIBUTERS
    # PLEASE USE YOUR OWN BOT TOKEN
    # CREATE .vscode/launch.json and add your token as an env
    # .vscode is gitignored so you do not need to remove it (however just to be safe you should remove it on commit)
    bot.run(os.environ['RELEASE_BOT_SECRET'])

if __name__ == '__main__':
    run()