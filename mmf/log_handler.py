import logging
import os

'''
1. Logger for all model outputs
Logs to collect all output from the models.
logger_allout = Logger(logger_name='all_output', level=logging.DEBUG, handler_name=('file'), 
logger_folder=logpath, formatter=vformatter).get_logger()
2. Logger for model metrics
Logs to collect important results and metrics.
logger_metrics = Logger(logger_name='metrics', level=logging.INFO, handler_name=('file'), 
logger_folder=logpath, formatter=vformatter).get_logger()
where:
logpath = os.getenv['LOCAL_LOGS’]

'''

# import nabds
# import logging
# from nabds.util import Logger
# from nabds.util import VersionFormatter
#
# logpath = os.environ['LOCAL_LOGS']
#
# logger_allout = logging.getLogger('all_output')
# logger_metrics = logging.getLogger('metrics')


class LogHandler(object):

    def __init__(self, config):

        #self.logger = logging.getLogger(__name__)

        logger = logging.getLogger(__name__)

        # TODO replace following when nabds starts working
        # self.logger_allout = logging.getLogger('all_output')
        # self.logger_metrics = logging.getLogger('metrics')

        # self.logger.setLevel(logging.DEBUG)
        #
        # # Create the Handler for logging data to a file
        logger_handler = logging.FileHandler(os.path.dirname(os.path.abspath(__file__)) + '/' + 'app.log')
        #logger_handler.setLevel(logging.DEBUG)
        #
        # # Create a Formatter for formatting the log messages
        logger_formatter = logging.Formatter('%(name)s - %(levelname)s - %(message)s')
        #
        # # Add the Formatter to the Handler
        #logger_handler.setFormatter(logger_formatter)
        #
        # # Add the Handler to the Logger
        #logger.addHandler(logger_handler)
        logger.info('Log Handler initialised')
        #self.logger.basicConfig(filemode="a")

        logging.basicConfig(filemode="a", filename=os.path.dirname(os.path.abspath(__file__)) + '/' + config['LOG_FILE'], format=config['LOG_FORMAT'], level=logging.DEBUG)
        logger.debug("hey ho ----------------------")

    def debug(self):
        self.logger.debug(self.msg)

    def info(self):
        logging.info(self.msg)

    def warning(self):
        logging.warning(self.msg)

    def error(self, e=None):
        # logging.basicConfig(filemode="a", filename=config.LOG_FILE, format=config.LOG_FILE_FORMAT,
        #                     level=logging.ERROR)

        logging.error(e, exc_info=True)




