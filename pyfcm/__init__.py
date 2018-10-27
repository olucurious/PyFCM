"""
PyFCM
"""

# TODO: Add explanation, why is it imported here?
import traceback

from .__meta__ import (
    __title__,
    __summary__,
    __url__,
    __version__,
    __author__,
    __email__,
    __license__
)
from .fcm import FCMNotification

__all__ = [
    "traceback", "FCMNotification", "__title__", "__summary__",
    "__url__", "__version__", "__author__", "__email__", "__license__"
]
