import inspect
import logging
import os
import sys
from pathlib import Path

from TestData.Environment import Environment
from TestData.GlobalVariables import GlobalVariables


class LoggerUtil:
    @staticmethod
    def getLogger(self):
        loggerName = inspect.stack()[1][3]
        logger = logging.getLogger(loggerName)
        # root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
        # path = root_path + r"\Reports\logfile.log"
        # print("Root path of project:", root_path)
        filehandler = logging.FileHandler(GlobalVariables.GoTo[Environment.LogFilePath])
        formatter = logging.Formatter("%(asctime)s :%(levelname)s :%(name)s :%(message)s")
        filehandler.setFormatter(formatter)

        logger.addHandler(filehandler)
        logger.setLevel(logging.INFO)
        return logger
