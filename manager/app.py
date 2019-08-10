import os
from manager import db, auth, model_handler
import logging
from flask import jsonify
from flask import Flask
from manager.scheduler import Scheduler
from manager.log_handler import LogHandler


logger = logging.getLogger(__name__)

app = Flask(__name__, instance_relative_config=True)
# app.register_blueprint(manager.scheduler)
app.config.from_mapping(
    SECRET_KEY='dev',
    DATABASE=os.path.join(app.instance_path, 'manager.sqlite'),
)
#
# if test_config is None:
#     # load the instance config, if it exists, when not testing
#     app.config.from_pyfile('config.py', silent=True)
# else:
#     # load the test config if passed in
#     app.config.from_mapping(test_config)

# ensure the instance folder exists
try:
    os.makedirs(app.instance_path)
except OSError:
    pass

db.init_app(app)
model_handler.init_app(app)

# apply the blueprints to the app
#app.register_blueprint(auth.bp)

@app.route('/start_scheduler')
def start_scheduler():
    try:
        scheduler_obj = Scheduler()
        scheduler_obj.start()
    except BaseException as e:
        LogHandler("This is my exception").error()

    return 'Scheduler started'

@app.route('/start_manager')
def start_manager():
    return 'SUCCESS'

@app.route('/api')
def api():
    return jsonify(username="aa",
                   email="bb")


if __name__ == '__main__':
    app.run(debug=True)

