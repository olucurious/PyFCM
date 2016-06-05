*****
PyFCM
*****


Python client for FCM - Firebase Cloud Messaging (Android & iOS)

Firebase Cloud Messaging (FCM) is the new version of GCM. It inherits the reliable and scalable GCM infrastructure, plus new features. GCM users are strongly recommended to upgrade to FCM.


Links
=====

- Project: https://github.com/olucurious/pyfcm
- PyPi: https://pypi.python.org/pypi/pyfcm/


Quickstart
==========

Install using pip:


::

    pip install pyfcm


PyFCM supports Android and iOS.


Example
---

Send notifications using the ``FCMNotification`` class:

.. code-block:: python
    # Send to single device.
    from pyfcm import FCMNotification

    push_service = FCMNotification(api_key="<api-key>")

    registration_id = "<device registration_id>"
    message = "Hi john, your Uber driver is around"
    result = push_service.notify_single_device(registration_id=registration_id, message_body=message)

    # Send to multiple devices by passing a list of ids.
    registration_ids = ["<device registration_id 1>", "<device registration_id 2>", ...]
    message = "Have you checked for cool Uber drivers around lately?"
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message)

    print result

Send a low priority message.

.. code-block:: python

    # The default is low_priority == False
    result = push_service.notify_multiple_devices(registration_ids=registration_ids, message_body=message, low_priority=True)


Access response data.

.. code-block:: python

    # Response from FCM Server.
    print result['multicast_id']
    print result['success']
    print result['failure']
    print result['canonical_ids']
    print result['results']
