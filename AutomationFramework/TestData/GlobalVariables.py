import os

from TestData.Environment import Environment


class GlobalVariables:
    GoTo = {
        Environment.Url: Environment.QA,
        Environment.LogFilePath: os.path.abspath(
            os.path.join(os.path.dirname(__file__), '..')) + r"\Reports\logfile.log"

    }
