# A special configuration file that is run
# before the test cases. This file is used
# to configure `pytest` so that dependent test
# cases are executed correctly.


def pytest_configure(config):
    # Standard Library
    import os

    # Set the APP_ENV to `test`
    os.environ["APP_ENV"] = "test"
