import os
import logging

from flask import Flask
from flask import jsonify

from mmf import db, model_handler
from mmf.log_handler import LogHandler
from mmf.scheduler import Scheduler


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    config = {
        "development": "config.DevelopmentConfig",
        "testing": "config.TestingConfig",
        "default": "config.DevelopmentConfig"
    }

    config_name = os.getenv('FLASK_CONFIG', 'default')
    app.config.from_object(config[config_name])  # object-based default configuration
    app.config.from_pyfile('config.cfg', silent=True)  # instance-folders configuration
    app.config.from_envvar('FLASK_SETTINGS') # env settings

    # initialize log handler with app config
    LogHandler(app.config)

    logger = logging.getLogger(__name__)
    logger.info('_______________________________________________________________')
    logger.info(f'MMF app created {__name__}')
    logger.info('MMF app configured')

    # config settings
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_mapping(
            SECRET_KEY=os.environ.get("SECRET_KEY"),
            DATABASE=os.path.join(app.instance_path, 'manager.sqlite'),
        )

    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    db.init_app(app)

    model_handler.init_app(app)
    logger.debug("model handler initialized")

    scheduler = Scheduler()
    scheduler.start_scheduler()
    logger.debug("scheduler initialized")

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except FileExistsError as e:
        LogHandler('Flask app instance folder missing').error(e)
        pass

    @app.route('/mmf_app')
    def api():
        logger.debug("mmf app api called")
        return jsonify(status="success")

    return app

