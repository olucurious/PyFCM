#!/usr/bin/env python
# -*- coding: utf-8 -*-
__author__ = 'olucurious'
from pyfcm import FCMNotification

push_service = FCMNotification(api_key="<api-key>")
registration_id="<device registration_id>"
message = "Hope you're having fun this weekend, don't forget to check today's news"
result = push_service.notify_topic_subscribers(topic_name="global", message_body=message)
print(result)
