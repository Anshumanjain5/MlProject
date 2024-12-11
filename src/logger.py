import logging
import os
from datetime import datetime

log_folder = f"{datetime.now().strftime('%Y-%m-%d')}"
log_dir = os.path.join(os.getcwd(), "logs", log_folder)
os.makedirs(log_dir, exist_ok=True)

log_file = f"{datetime.now().strftime('%Y-%m-%d %I-%M-%S-%p')}.log"
log_file_path = os.path.join(log_dir, log_file)

logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='[ %(asctime)s ] - %(lineno)d - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)
