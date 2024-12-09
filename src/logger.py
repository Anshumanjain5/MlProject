import logging
import os
from datetime import datetime

# Create a folder for today's logs
log_folder = f"{datetime.now().strftime('%Y-%m-%d')}"
log_dir = os.path.join(os.getcwd(), "logs", log_folder)
os.makedirs(log_dir, exist_ok=True)

# Ensure unique log file names
log_file = f"{datetime.now().strftime('%Y-%m-%d %I-%M-%S-%p')}.log"
log_file_path = os.path.join(log_dir, log_file)

# Configure logging to file and console
logging.basicConfig(
    filename=log_file_path,
    level=logging.INFO,
    format='[ %(asctime)s ] - %(lineno)d - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

# Add a console handler
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('[ %(asctime)s ] - %(message)s'))
logging.getLogger().addHandler(console_handler)

if __name__ == "__main__":
    logging.info("Logging has started")
