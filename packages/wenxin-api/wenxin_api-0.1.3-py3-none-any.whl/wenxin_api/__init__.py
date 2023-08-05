""" wenxin api python bindings. """


import os
from typing import Optional
from wenxin_api.base_object import BaseObject
from wenxin_api.api import Task, Dataset, Train, Model
from wenxin_api.error import WenxinError, APIError, InvalidRequestError
from wenxin_api.requestor import WenxinAPIResponse
from wenxin_api.variable import ak, sk, access_token, proxy, debug
from wenxin_api import const, log

version_contents = {}
version_path = os.path.join(
    os.path.abspath(os.path.dirname(__file__)), "version.txt"
)
with open(version_path, "rt") as f:
    exec(f.read(), version_contents)
version = version_contents["VERSION"]

__all__ = [
    "Task"
    "Dataset",
    "Train",
    "Model",
    "BaseObject",
    "APIError",
    "WenxinError",
    "InvalidRequestError",
    "ak",
    "sk",
    "version",
    "access_token",
    "api_type",
    "log",
    "const"
]