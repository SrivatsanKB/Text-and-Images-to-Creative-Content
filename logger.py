import logging
import os
import datetime

# Get the current timestamp
timestamp = datetime.datetime.now().strftime('%m_%d_%Y_%H_%M_%S')

# Create a directory for logs if it does not exist
logs_dir = os.path.join(os.getcwd(), "logs")
os.makedirs(logs_dir, exist_ok=True)

# Create the log file path
LOG_FILE = f"{timestamp}.log"
LOG_FILE_PATH = os.path.join(logs_dir, LOG_FILE)

# Configure logging
logging.basicConfig(
    filename=LOG_FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)

# Example usage
logging.info("Logger is configured.")
