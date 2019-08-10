from manager.log_handler import LogHandler
import click
from flask.cli import with_appcontext
from manager.sentiment import app

def init_app(app):
    app.cli.add_command(run_model_command)


def run_model():
    result_json = app.run_model()
    LogHandler("run model called --------------- json = ").debug()
    LogHandler(result_json).debug()
    return result_json


@click.command('run-model')
@with_appcontext
def run_model_command():
    """Clear the existing data and create new tables."""
    result_json = run_model()
    click.echo(result_json)
