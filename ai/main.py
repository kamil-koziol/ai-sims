import logging
import config.general
from api import App

logging.basicConfig(
    filename=config.general.LOG_FILE_NAME,
    filemode="w",
    encoding="utf-8",
    level=config.general.LOGGING_LEVEL,
    format="%(levelname)s: %(message)s",
)
api = App()
api.run("0.0.0.0", 80)
logging.info("Application started")
