import schedule
import time
from manager.log_handler import LogHandler
import manager.model_handler


# https://schedule.readthedocs.io/
# https://pypi.org/project/schedule/
#scheduler = Blueprint('simple_page', __name__,
#                        template_folder='templates')


class Scheduler:
    def __init__(self):
        LogHandler("scheduler initialized.........").debug()
        schedule.every(1).minutes.do(self.job)

    def job(self):
        LogHandler("Scheduler job started job XXX..........").debug()
        manager.model_handler.run_model()

    def start(self):
        while True:
            schedule.run_pending()
            time.sleep(1)


# schedule.every().hour.do(job)
# schedule.every().day.at("10:30").do(job)
# schedule.every(5).to(10).minutes.do(job)
# schedule.every().monday.do(job)
# schedule.every().wednesday.at("13:15").do(job)
# schedule.every().minute.at(":17").do(job)
