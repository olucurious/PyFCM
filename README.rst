*****
PyFCM
*****

Python client for FCM - Firebase Cloud Messaging (Android & iOS)

Firebase Cloud Messaging (FCM) is the new version of GCM. It inherits the reliable and scalable GCM infrastructure, plus new features. GCM users are strongly recommended to upgrade to FCM.

Using FCM, you can notify a client app that new email or other data is available to sync. You can send notifications to drive user reengagement and retention. For use cases such as instant messaging, a message can transfer a payload of up to 4KB to a client app.

For more information, visit: https://firebase.google.com/docs/cloud-messaging/


Links
=====

- Project: https://github.com/olucurious/pyfcm
- PyPi: https://pypi.python.org/pypi/pyfcm/


Quickstart
==========

Install using pip:


::

    pip install pyfcm

    OR

    pip install git+https://github.com/olucurious/PyFCM.git

PyFCM supports Android and iOS.

Examples
--------

Send notifications using the ``FCMNotification`` class:

.. code-block:: python

    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="<api-key>")

    # OR initialize with proxies

    proxy_dict = {
              "http"  : "http://127.0.0.1",
              "https" : "http://127.0.0.1",
            }
    push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict)

    # Your api-key can be gotten from:  https://console.firebase.google.com/project/<project-name>/settings/cloudmessaging

    registration_id = "<device registration_id>"
    message_title = "Uber update"
    message_body = "Hi john, your customized news for today is ready"
    result = push_service.notify_single_device(registration_id=registration_id, message_title=message_title, message_body=message_body)

    # Send to multiple devices by passing a list of ids.
    registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
    message_title = "Uber update"
    message_body = "Hope you're having fun this weekend, don't forget to check today's news"
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_title=message_title, message_body=message_body)

    print result

Send a data message.

.. code-block:: python

    # With FCM, you can send two types of messages to clients:
    # 1. Notification messages, sometimes thought of as "display messages."
    # 2. Data messages, which are handled by the client app.

    # Client app is responsible for processing data messages. Data messages have only custom key-value pairs. (Python dict)
    # Data messages let developers send up to 4KB of custom key-value pairs.

    # Sending a notification with data message payload
    data_message = {
        "Nick" : "Mario",
        "body" : "great match!",
        "Room" : "PortugalVSDenmark"
    }
    # To multiple devices
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message_body, data_message=data_message)
    # To a single device
    result = push_service.notify_single_device(registration_id=registration_id, message_body=message_body, data_message=data_message)

    # Sending a data message only payload, do NOT include message_body
    # To multiple devices
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, data_message=data_message)
    # To a single device
    result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message)

    # Use notification messages when you want FCM to handle displaying a notification on your app's behalf.
    # Use data messages when you just want to process the messages only in your app.
    # PyFCM can send a message including both notification and data payloads.
    # In such cases, FCM handles displaying the notification payload, and the client app handles the data payload.

Send a low priority message.

.. code-block:: python

    # The default is low_priority == False
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message, low_priority=True)

Sending a message to a topic.

.. code-block:: python

    # Send a message to devices subscribed to a topic.
    result = push_service.notify_topic_subscribers(topic_name="news", message_body=message)

    # Conditional topic messaging
    topic_condition = "'TopicA' in topics && ('TopicB' in topics || 'TopicC' in topics)"
    result = push_service.notify_topic_subscribers(message_body=message, condition=topic_condition)
    # FCM first evaluates any conditions in parentheses, and then evaluates the expression from left to right.
    # In the above expression, a user subscribed to any single topic does not receive the message. Likewise,
    # a user who does not subscribe to TopicA does not receive the message. These combinations do receive it:
    # TopicA and TopicB
    # TopicA and TopicC
    # Conditions for topics support two operators per expression, and parentheses are supported.
    # For more information, check: https://firebase.google.com/docs/cloud-messaging/topic-messaging

Other argument options

::

    
    collapse_key (str, optional): Identifier for a group of messages
        that can be collapsed so that only the last message gets sent
        when delivery can be resumed. Defaults to `None`.
    delay_while_idle (bool, optional): If `True` indicates that the
        message should not be sent until the device becomes active.
    time_to_live (int, optional): How long (in seconds) the message
        should be kept in FCM storage if the device is offline. The
        maximum time to live supported is 4 weeks. Defaults to ``None``
        which uses the FCM default of 4 weeks.
    low_priority (boolean, optional): Whether to send notification with
        the low priority flag. Defaults to `False`.
    restricted_package_name (str, optional): Package name of the
        application where the registration IDs must match in order to
        receive the message. Defaults to `None`.
    dry_run (bool, optional): If `True` no message will be sent but
        request will be tested.

Access response data.

.. code-block:: python

    # Response from FCM Server.
    print result['multicast_id'] #Unique ID (number) identifying the multicast message.
    print result['success'] #Number of messages that were processed without an error.
    print result['failure'] #Number of messages that could not be processed.
    print result['canonical_ids'] #Number of results that contain a canonical registration token.
    print result['results'] #Array of objects representing the status of the messages processed.

    # The result objects are listed in the same order as the request (i.e., for each registration ID in the request,
    # its result is listed in the same index in the response).
    # message_id: String specifying a unique ID for each successfully processed message.
    # registration_id: Optional string specifying the canonical registration token for the client app that the message
    # was processed and sent to. Sender should use this value as the registration token for future requests. Otherwise,
    # the messages might be rejected.
    # error: String specifying the error that occurred when processing the message for the recipient
    
    
License
-------

The MIT License (MIT). Please see LICENSE.rst for more information.


::

    Copyright (c) 2016 Emmanuel Adegbite

    Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation
    files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy,
    modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software
    is furnished to do so, subject to the following conditions:

    The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.

    THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
    OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
    LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR
    IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


.. |version| image:: http://img.shields.io/pypi/v/pyfcm.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyfcm/

.. |license| image:: http://img.shields.io/pypi/l/pyfcm.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyfcm/


