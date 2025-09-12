import logging
import traceback
from datetime import datetime


from infrastructure.logger_sys.fluentd.fluentd_api import FluentdAPI


class FluentdHandler(logging.Handler):

    def __init__(self) -> None:
        self.sender = FluentdAPI("identity.service")
        logging.Handler.__init__(self=self)

    def emit(self, record) -> None:
        self.sender.send(record.funcName, {
            "message": record.message,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "level": record.levelname,
            "traceback": traceback.format_exc(),
        })