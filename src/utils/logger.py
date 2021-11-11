import dotenv
import logging
import logging_loki
import os
from env import get_env_file

logger = logging.getLogger("discord")
logger.setLevel(logging.DEBUG)


def add_handlers():
    global logger
    dotenv.load_dotenv(get_env_file())

    user = os.environ.get("GRAFANA_USER")
    password = os.environ.get("GRAFANA_PASS")

    file_handler = logging.FileHandler(
        filename="discord.log", encoding="utf-8", mode="w")
    console_handler = logging.StreamHandler()

    console_handler.setLevel(logging.INFO)
    file_handler.setLevel(logging.DEBUG)

    file_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )
    console_handler.setFormatter(
        logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
    )

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    if user is not None and password is not None:
        loki_handler = logging_loki.LokiHandler(
            url="https://logs-prod-us-central1.grafana.net/loki/api/v1/push",
            tags={"application": "renft-discord-bot"},
            auth=(user, password),
            version="1",
        )
        loki_handler.setLevel(logging.DEBUG)
        loki_handler.setFormatter(
            logging.Formatter("%(asctime)s:%(levelname)s:%(name)s: %(message)s")
        )

        logger.addHandler(loki_handler)
