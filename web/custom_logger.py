import logging
from reNgine.common_func import send_slack_message
import os


class NotifyLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.setLevel(logging.DEBUG)

    def emit(self, record):
        log_entry = self.format(record)
        send_slack_message(log_entry, channel=os.getenv("SLACK_ERROR_LOG_CHANNEL"))
