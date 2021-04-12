import logging
import sys


def create_logger(name):
    """
    Creates logging instance that will be available in the whole project scope
    :param name: Name of the logging instance that needs to be created and configured.
    :return: Logger instance with attached StreamHandler.
    """

    logger = logging.getLogger(name)
    logger.setLevel(10)

    stream_handler = logging.StreamHandler(stream=sys.stdout)
    stream_handler.setLevel(10)
    stream_handler.setFormatter(
        logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    )

    logger.addHandler(stream_handler)

    # Block the propagation of logging messages to root logger
    logger.propagate = False

    return logger
