import inspect
import logging

import pytest


@pytest.mark.usefixtures("Setup")
class BaseClass:
    pass


