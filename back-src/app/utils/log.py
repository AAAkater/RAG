import logging
import sys
from logging import Logger

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(stream=sys.stdout),
        # logging.FileHandler("app.log", mode="a"),
    ],
)

logger: Logger = logging.getLogger("fastapi")
