from pyfcm import FCMNotification
from pyfcm.v1.baseapi import BaseAPI

class FCMNotification(FCMNotification, BaseAPI):
    def __init__(self, *args, **kwargs):
        super(BaseAPI).__init__(*args, **kwargs)
