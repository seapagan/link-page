"""Set up logging."""

import logging
import sys

logger = logging.getLogger()

# create formatter
formatter = logging.Formatter(fmt="%(levelname)s:     %(message)s")

# create handler
stream_handler = logging.StreamHandler(sys.stdout)

# add formatter to stream_handler
stream_handler.setFormatter(formatter)

# add handler to logger
logger.handlers = [stream_handler]

# set logging level
logger.setLevel(logging.INFO)
