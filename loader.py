import logging
from colorama import Fore
skipped_cogs = ['example-cog']

async def loader(bot,type,cog_name):
    if type == 'load':
        try:
            if cog_name not in bot.cogs:
                if cog_name in skipped_cogs:
                    logging.info(Fore.YELLOW+f'Skipped loading {cog_name}')
                    return 1
                logging.info(Fore.BLUE+'Loading '+cog_name)
                await bot.load_extension(f"cogs.{cog_name}")
                logging.info(Fore.GREEN+'Loaded ' + cog_name)
                return 0
        except Exception as e:
            logging.critical(Fore.RED+f'Failed to load {cog_name} {e}')
            logging.info(Fore.YELLOW+f'Skipped loading {cog_name}')
            return 2
    elif type == 'unload':
        try:
            if cog_name in bot.cogs:
                if cog_name in skipped_cogs:
                    logging.info(Fore.YELLOW+f'Skipped unloading {cog_name}')
                    return 1
                logging.info(Fore.BLUE+'Unloading '+cog_name)
                await bot.unload_extension(f"cogs.{cog_name}")
                logging.info(Fore.GREEN+'Unloaded ' + cog_name)
                return 0
        except Exception as e:
            logging.critical(Fore.RED+f'Failed to unload {cog_name} {e}')
            logging.info(Fore.YELLOW+f'Skipped unloading {cog_name}')
            return 2