import logging
import config


class LogHandler(object):

    def __init__(self, msg):

        self.msg = msg
        self.logger = logging.getLogger(__name__)

    def debug(self):

        logging.basicConfig(filemode="a", filename=config.LOG_FILE, format=config.LOG_FILE_FORMAT, level=logging.DEBUG)
        logging.debug(self.msg)

    def error(self, e=None):
        logging.basicConfig(filemode="a", filename=config.LOG_FILE, format=config.LOG_FILE_FORMAT,
                            level=logging.ERROR)
        #logging.exception(self.msg)
        logging.error(e, exc_info=True)
        # self.logger.setLevel(logging.DEBUG)
        #
        # # Create the Handler for logging data to a file
        # logger_handler = logging.FileHandler('python_logging.log')
        # logger_handler.setLevel(logging.DEBUG)
        #
        # # Create a Formatter for formatting the log messages
        # logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        #
        # # Add the Formatter to the Handler
        # logger_handler.setFormatter(logger_formatter)
        #
        # # Add the Handler to the Logger
        # self.logger.addHandler(logger_handler)
        # self.logger.info('Log Handler initialised')



