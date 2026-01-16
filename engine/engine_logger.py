import logging
from pathlib import Path

LOG_DIR = Path("logs")
LOG_DIR.mkdir(exist_ok=True)

ENGINE_LOG_FILE = LOG_DIR / "engine.log"

logger = logging.getLogger("ENGINE")
logger.setLevel(logging.INFO)

if not logger.handlers:
    handler = logging.FileHandler(ENGINE_LOG_FILE, encoding="utf-8")
    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    handler.setFormatter(formatter)
    logger.addHandler(handler)

def get_engine_logger() -> logging.Logger:
    return logger
