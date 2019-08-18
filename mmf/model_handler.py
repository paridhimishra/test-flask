import importlib
import logging
import click
from flask.cli import with_appcontext
from datetime import datetime
from mmf.log_handler import LogHandler
from mmf.exception import ModelNotFoundError, ModelRunFailedError

logger = logging.getLogger(__name__)

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

    try:
        model_main = importlib.import_module('mmf' + '.' + model + '.' + 'main')
    except ModuleNotFoundError as e:
        logger.error(f'Module missing for model = {model}', e)
        return { 'status': 'fail'}

    try:
        model_main.run_model()
    except ModelRunFailedError as e:
        logger.error(f'Model failed to run for model = {model}', e)
        return { 'status': 'fail'}

    result_json = {'execution_time': datetime.now().strftime("%d/%m/%Y %H:%M:%S"), 'status': 'success'}
    logger.debug(f' Running {model}, execution result is {result_json}')
    return result_json


@click.command('run-model')
@with_appcontext
def run_model_command():
    """Clear the existing data and create new tables."""
    result_json = run_model()
    click.echo(result_json)
