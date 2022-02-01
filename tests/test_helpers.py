import json
from contextlib import contextmanager

import pytest


def get_test_data_from_json_file(filename):
    with open(filename, "r") as file:
        test_data = json.load(file)
    return test_data


@contextmanager
def not_raises(exception_cls, msg=""):
    """
    Function that acts similar to pytest's raises
    """
    try:
        yield
    except exception_cls as exc:
        raise pytest.fail(f"Did raise {exception_cls} - {exc}. {msg}")
