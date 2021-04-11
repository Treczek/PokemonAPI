import json
import logging
import sys

from flask import Response


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


def replace_id_field_in_response(response: Response):
    """
    MongoDB doesn't allow to use 'id' as a field name.
    Considering that we have such requirement, we need to change the respond object before passing it to the client.

    :param response: Respond object with data contaning b-jsons with '_id' fields
    :return: Response with altered 'data' parameter
    """

    response.data = json.dumps(  # Convert from binary json to dictionary
                        json.loads(response.data)  # Encode dictionary to string
                    ).replace('"_id":', '"id":')

    return response
