import importlib
import logging
import click
import boto3
import os

from flask.cli import with_appcontext
from datetime import datetime
from mmf.log_handler import LogHandler
from mmf.exception import ModelNotFoundError, ModelRunFailedError

logger = logging.getLogger(__name__)
# Create CloudWatch client
cloudwatch = boto3.client('cloudwatch', region_name='ap-southeast-2',
                          aws_access_key_id=os.environ.get("AWS_ACCESS_KEY_ID"),
                          aws_secret_access_key=os.environ.get("AWS_SECRET_ACCESS_KEY"))

def init_app(app):
    app.cli.add_command(run_model_command)


def run_model(model) -> dict:
    '''
    before running
    :return:
    '''

    if not model:
        logger.error('Model name empty in run_model()')
        raise ModelNotFoundError

    model_execution_status = {'execution_time': datetime.now().strftime("%d/%m/%Y %H:%M:%S")}
    try:
        model_main = importlib.import_module('mmf' + '.' + model + '.' + 'main')
    except ModuleNotFoundError as e:
        logger.error(f'Module missing for model = {model}', e)
        model_execution_status['status'] = 'fail'
        return model_execution_status

    try:
        model_result = model_main.run_model()
    except ModelRunFailedError as e:
        logger.error(f'Model failed to run for model = {model}', e)
        model_execution_status['status'] = 'fail'
        return model_execution_status

    model_execution_status['status'] = 'pass'
    model_execution_status['model_result'] = model_result
    logger.debug(f' Running {model}, execution result is {model_execution_status}')

    # Put custom metrics
    cloudwatch.put_metric_data(
        MetricData=[
            {
                'MetricName': model,
                'Dimensions': [
                    {
                        'Name': 'UNIQUE_PAGES',
                        'Value': 'URLS'
                    },
                ],
                'Unit': 'None',
                'Value': model_execution_status['model_result']['confidence']
            },
        ],
        Namespace='MMF'
    )
    return model_execution_status


@click.command('run-model')
@with_appcontext
def run_model_command():
    """Clear the existing data and create new tables."""
    result_json = run_model()
    click.echo(result_json)
