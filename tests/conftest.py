# Standard Library
import os


def pytest_generate_tests(metafunc):
    os.environ["APP_ENV"] = "test"
