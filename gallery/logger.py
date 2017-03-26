import logging
import os

LOG_FOLDER = "log"

if not os.path.exists(LOG_FOLDER):
    os.mkdir(LOG_FOLDER)


class BellLogger:
    def __init__(self, name, file_name=None, default_level="INFO"):
        if not file_name:
            file_name = "{}.log".format(name)
        self.logger = logging.getLogger(name)
        if not os.path.exists(os.path.join(LOG_FOLDER, file_name)):
            open(file_name, 'a').close()

        brl_fl_hndlr = logging.FileHandler(os.path.join(LOG_FOLDER, file_name))
        self.logger.addHandler(brl_fl_hndlr)
        self.logger.setLevel(getattr(logging, default_level))

    def log(self, message, level="INFO"):
        self.logger.log(getattr(logging, level), message)
