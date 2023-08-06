# Package pii_optimized_logger

Configuration:

log_disable_handler
value 0 is the default value and the handler is enable
value 1 will disable the handler


log_max_length

default value is 50000
it is used to define the max length for each message to print in log



# Sample to use the library

import logging
from pii_optimized_logger import log_handler

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

logger.handlers = log_handler.create()