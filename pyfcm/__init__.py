"""
PyFCM

"""

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

try:
    from .extensions.tornado import TornadoFCMNotification
except ImportError:
    pass
