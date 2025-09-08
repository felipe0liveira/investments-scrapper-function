import logging
from dotenv import load_dotenv
import os


class Settings:
    def __init__(self):
        load_dotenv()
        self.GOOGLE_APPLICATION_CREDENTIALS = os.getenv(
            "GOOGLE_APPLICATION_CREDENTIALS"
        )

        log_format = logging.Formatter(
            "%(asctime)s [%(levelname)s] %(name)s: %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S"
        )

        file_handler = logging.FileHandler("app.log", mode="w")
        file_handler.setFormatter(log_format)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(log_format)

        logging.basicConfig(level=logging.INFO, handlers=[file_handler, console_handler])
