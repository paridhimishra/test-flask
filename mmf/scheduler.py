import time
import os
import schedule

import logging

import mmf.model_handler
from mmf.exception import SchedulerNotFoundError, SchedulerNotRunningError

import json

'''
'''
logger = logging.getLogger(__name__)


class Scheduler:

    def __init__(self):
        logger.debug("Scheduler initialized.........")
        self.schedule = schedule

    def schedule_jobs(self, mmf_config):
        '''

        :return:
        '''

        models = mmf_config['models']
        for model in models:

            model_schedule_type = mmf_config['models'][model]['schedule_type']
            model_schedule_interval = mmf_config['models'][model]['schedule_interval']

            try:
                if model_schedule_type == 'day':
                    self.schedule.every(int(model_schedule_interval)).day.do(mmf.model_handler.run_model, model)

                elif model_schedule_type == 'hour':
                    self.schedule.every(int(model_schedule_interval)).hours.do(mmf.model_handler.run_model, model)

                elif model_schedule_type == 'minutes':
                    self.schedule.every(int(model_schedule_interval)).minutes.do(mmf.model_handler.run_model, model)

                else:
                    raise SchedulerNotFoundError

            except SchedulerNotFoundError as e:
                logger.error(f'Schedule for {model} %s not found in mmf_config', e)

            logger.debug(f'Schedule for {model} set for {model_schedule_interval} {model_schedule_type} ')

        return

    def run_scheduled_jobs(self):
        '''

        :return:
        '''
        return
        # for model in models:
        #     mmf.model_handler.run_model(model)
        #     LogHandler('Scheduler job started for model %s'.format(model)).info()

    def start_scheduler(self):
        '''

        :return:
        '''
        scheduler = Scheduler()

        # get model info
        with open(os.path.join(os.path.dirname(__file__), 'mmf_config.json'), 'rb') as config_file:
            mmf_config = json.load(config_file)

        scheduler.schedule_jobs(mmf_config)
        logger.debug("schedule set for models")

        try:
            scheduler.run_scheduled_jobs()
        except SchedulerNotRunningError as e:
            logger.error("Scheduler failed to run ", e)
            return

        logger.info('Scheduler started running jobs')

        while True:
            schedule.run_pending()
            time.sleep(mmf_config['scheduler']['sleep_interval'])
