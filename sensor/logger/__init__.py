import os
import logging
from datetime import datetime
from from_root import from_root

LOG_FILE_NAME = f"{datetime.now().strftime('%d%m%Y_%H%M%S')}.log"

LOG_DIR = os.path.join(from_root(),"logs",LOG_FILE_NAME)

os.makedirs(LOG_DIR, exist_ok=True)

LOG_FILE_PATH = os.path.join(LOG_DIR, LOG_FILE_NAME)

logging.basicConfig(
    filename=LOG_FILE_PATH
    , format='[%(asctime)s]_%(levelname)s: ~%(message)s~'
    ,level=logging.INFO
)