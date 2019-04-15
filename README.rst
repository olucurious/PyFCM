*****
PyFCM
*****
|version| |license| 

Python client for FCM - Firebase Cloud Messaging (Android, iOS and Web)

Firebase Cloud Messaging (FCM) is the new version of GCM. It inherits the reliable and scalable GCM infrastructure, plus new features. GCM users are strongly recommended to upgrade to FCM.

Using FCM, you can notify a client app that new email or other data is available to sync. You can send notifications to drive user reengagement and retention. For use cases such as instant messaging, a message can transfer a payload of up to 4KB to a client app.

For more information, visit: https://firebase.google.com/docs/cloud-messaging/


Links
=====

- Project: https://github.com/olucurious/pyfcm
- PyPi: https://pypi.python.org/pypi/pyfcm/

Looking for a Django version?
-----------------------------
Checkout fcm-django
- Link: https://github.com/xtrinch/fcm-django

Updates (Breaking Changes)
--------------------------

- MAJOR UPDATES (AUGUST 2017): https://github.com/olucurious/PyFCM/releases/tag/1.4.0


Quickstart
==========

Install using pip:


::

    pip install pyfcm

    OR

    pip install git+https://github.com/olucurious/PyFCM.git

PyFCM supports Android, iOS and Web.

Features
--------

- All FCM functionality covered
- Tornado support


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
    # 3. Notification messages with optional data payload.

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

    # Sending a data message only payload, do NOT include message_body also do NOT include notification body
    # To multiple devices
    result = push_service.multiple_devices_data_message(registration_ids=registration_ids, data_message=data_message)
    # To a single device
    result = push_service.single_device_data_message(registration_id=registration_id, data_message=data_message)

    # To send extra kwargs (notification keyword arguments not provided in any of the methods),
    # pass it as a key value in a dictionary to the method being used
    extra_notification_kwargs = {
        'android_channel_id': 2
    }
    result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message, extra_notification_kwargs=extra_notification_kwargs)

    # To process background notifications in iOS 10, set content_available
    result = push_service.notify_single_device(registration_id=registration_id, data_message=data_message, content_available=True)

    # To support rich notifications on iOS 10, set
    extra_kwargs = {
        'mutable_content': True
    }
    

    
    
    
    # and then write a NotificationService Extension in your app

    # Use notification messages when you want FCM to handle displaying a notification on your app's behalf.
    # Use data messages when you just want to process the messages only in your app.
    # PyFCM can send a message including both notification and data payloads.
    # In such cases, FCM handles displaying the notification payload, and the client app handles the data payload.

Send a low priority message.

.. code-block:: python

    # The default is low_priority == False
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message, low_priority=True)

Get valid registration ids (useful for cleaning up invalid registration ids in your database)

.. code-block:: python

    registration_ids = ['reg id 1', 'reg id 2', 'reg id 3', 'reg id 4', ...]
    valid_registration_ids = push_service.clean_registration_ids(registration_ids)
    # Shoutout to @baali for this

Appengine users should define their environment

.. code-block:: python

    push_service = FCMNotification(api_key="<api-key>", proxy_dict=proxy_dict, env='app_engine')
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message, low_priority=True)
    
Manage subscriptions to a topic

.. code-block:: python

    push_service = FCMNotification(SERVER_KEY)
    tokens = [
        <registration_id_1>,
        <registration_id_2>,
    ]
    
    subscribed = push_service.subscribe_registration_ids_to_topic(tokens, 'test')
    # returns True if successful, raises error if unsuccessful

    unsubscribed = push_service.unsubscribe_registration_ids_from_topic(tokens, 'test')
    # returns True if successful, raises error if unsuccessful

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

Get response data.

.. code-block:: python

    # Response from PyFCM.
    response_dict = {
        'multicast_ids': list(), # List of Unique ID (number) identifying the multicast message.
        'success': 0, #Number of messages that were processed without an error.
        'failure': 0, #Number of messages that could not be processed.
        'canonical_ids': 0, #Number of results that contain a canonical registration token.
        'results': list(), #Array of dict objects representing the status of the messages processed.
        'topic_message_id': None or str
    }

    # registration_id: Optional string specifying the canonical registration token for the client app that the message
    # was processed and sent to. Sender should use this value as the registration token for future requests. Otherwise,
    # the messages might be rejected.
    # error: String specifying the error that occurred when processing the message for the recipient
    
    
.. |version| image:: http://img.shields.io/pypi/v/pyfcm.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyfcm/

.. |license| image:: http://img.shields.io/pypi/l/pyfcm.svg?style=flat-square
    :target: https://pypi.python.org/pypi/pyfcm/


