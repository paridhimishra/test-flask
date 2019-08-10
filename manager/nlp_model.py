from manager.log_handler import LogHandler
import click
from flask.cli import with_appcontext


def init_app(app):
    app.cli.add_command(run_model_command)


def run_model():
    LogHandler("run model called --------------- this code has to reach cloudwatch ").debug()
    return


@click.command('run-model')
@with_appcontext
def run_model_command():
    """Clear the existing data and create new tables."""
    run_model()
    click.echo('Running the model from cmd line')
