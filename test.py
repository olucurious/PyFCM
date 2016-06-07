#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'olucurious'
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="<api-key>")
registration_id="<device registration_id>"
message = "Hi john, your Uber driver is around"
result = push_service.notify_single_device(registration_id=registration_id, message_body=message)
print result
