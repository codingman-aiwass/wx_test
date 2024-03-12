# log_config.py
import logging


def setup_logging():
    logger = logging.getLogger('my_app')
    logger.setLevel(logging.DEBUG)  # Set the minimum logging level

    # Create console handler and set level to INFO
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.INFO)
    console_format = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_format)

    # Create file handler and set level to DEBUG
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    file_format = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_format)

    # Add handlers to logger
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)


# Call setup_logging() to configure logger at module level
setup_logging()
