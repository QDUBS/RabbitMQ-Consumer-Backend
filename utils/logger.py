import logging

# Configure the logging format
LOG_FORMAT = '%(asctime)s - %(message)s'


# Create a logger
LOGGER = logging.getLogger(__name__)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(LOG_FORMAT)
console_handler.setFormatter(formatter)


LOGGER.addHandler(console_handler)


LOGGER.setLevel(logging.DEBUG)
