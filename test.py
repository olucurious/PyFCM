#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'olucurious'
from pyfcm import FCMNotification
from pprint import pprint
push_service = FCMNotification(api_key="<server key>")
registration_id="<device registration_id>"
message = "Hope you're having fun this weekend, don't forget to check today's news"
result = push_service.notify_single_device(registration_id=registration_id)
pprint(result)
result = push_service.notify_multiple_devices(registration_ids=[registration_id,registration_id,registration_id])
pprint(result)
result = push_service.notify_topic_subscribers(topic_name="global", message_body=message)
pprint(result)
