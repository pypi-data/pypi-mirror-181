import logging
import loguru

#########################################

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)


class LoguruInterceptHandler(logging.Handler):
    """Enable loguru logging."""

    def emit(self, record):

        try:
            level = logger.level(record.levelname).name
        except:
            level = record.levelno

        frame, depth = logging.currentframe(), 2
        while frame.f_code.co_filename == logging.__file__:
            frame = frame.f_back
            depth += 1

        # process message
        message = record.getMessage()
        new_message = ""
        words = message.split()
        for item in words:
            if len(item) >= 4:
                item_masked = "**" + item[2:]
            elif len(message) >= 2:
                item_masked = "**" + item[1:]
            new_message += item_masked + " "

        loguru.logger.opt(depth=depth, exception=record.exc_info).log(
            logging.getLevelName(level), new_message)



def create_handler():


    new_handler = [LoguruInterceptHandler()]  # overwrite old handlers

    return new_handler

#logger.handlers = new_handler
