from dynaconf import Dynaconf
from pathlib import Path
from dotenv import load_dotenv
import logging.config

load_dotenv(verbose=True)

BASE_DIR = Path(__file__).parent.parent

settings = Dynaconf(
    settings_files=[BASE_DIR / "settings.default.yaml"],
    environments=True,
    BASE_DIR=BASE_DIR,
)

log_dir = Path('/tmp/var/log/lowcode')
if not log_dir.exists():
    log_dir.mkdir(parents=True)

logging.config.dictConfig(settings.get("log", {}))
