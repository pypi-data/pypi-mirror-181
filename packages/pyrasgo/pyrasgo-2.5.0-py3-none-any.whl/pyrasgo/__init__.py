import logging
import webbrowser
import warnings

import requests

from pyrasgo import errors
from pyrasgo.config import set_session_api_key
from pyrasgo.version import __version__

__all__ = [
    '__version__',
    'connect',
    'open_docs',
    'pronounce_rasgo',
    'login',
]


def connect(api_key):
    from pyrasgo.rasgo import Rasgo

    try:
        version_check()
    except Exception:
        pass  # Don't error if we can't reach or understand pypi

    set_session_api_key(api_key)
    return Rasgo()


def open_docs():
    webbrowser.open("https://docs.rasgoml.com/rasgo-docs/reference/pyrasgo")


def pronounce_rasgo():
    webbrowser.open("https://www.spanishdict.com/pronunciation/rasgo?langFrom=es")


def login(email: str, password: str):
    from pyrasgo.api.login import Login
    from pyrasgo.schemas.user import UserLogin

    payload = UserLogin(
        email=email,
        password=password,
    )
    try:
        response = Login().login(payload=payload)
        return connect(api_key=response)
    except Exception as err:
        raise errors.APIError("Unable to log in with credentials provided") from err


def version_check():
    latest = requests.get("https://pypi.org/pypi/pyrasgo/json", timeout=5).json()["info"]["version"]
    if latest != __version__:
        warnings.warn(
            f"There is a newer version of PyRasgo Available ({latest}), "
            f"please upgrade to avoid any incompatibilities"
        )
