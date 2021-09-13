import logging

logger = logging.getLogger('discord')
logger.setLevel(logging.DEBUG)

file_handler = logging.FileHandler(
    filename='discord.log', encoding='utf-8', mode='w')
console_handler = logging.StreamHandler()

console_handler.setLevel(logging.INFO)
file_handler.setLevel(logging.DEBUG)

file_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))
console_handler.setFormatter(logging.Formatter(
    '%(asctime)s:%(levelname)s:%(name)s: %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)
