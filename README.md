# PyFCM

[![version](http://img.shields.io/pypi/v/pyfcm.svg?style=flat-square)](https://pypi.python.org/pypi/pyfcm/)
[![license](http://img.shields.io/pypi/l/pyfcm.svg?style=flat-square)](https://pypi.python.org/pypi/pyfcm/)

Python client for FCM - Firebase Cloud Messaging (Android, iOS and Web)

Firebase Cloud Messaging (FCM) is the new version of GCM. It inherits
the reliable and scalable GCM infrastructure, plus new features. GCM
users are strongly recommended to upgrade to FCM.

Using FCM, you can notify a client app that new email or other data is
available to sync. You can send notifications to drive user reengagement
and retention. For use cases such as instant messaging, a message can
transfer a payload of up to 4KB to a client app.

For more information, visit:
<https://firebase.google.com/docs/cloud-messaging/>

## Links

-   Project: <https://github.com/olucurious/pyfcm>
-   PyPi: <https://pypi.python.org/pypi/pyfcm/>

### Updates (Breaking Changes)

-   MIGRATION TO FCM HTTP V1 (JUNE 2024):
    <https://github.com/olucurious/PyFCM/releases/tag/2.0.0> (big
    shoutout to @Subhrans for the PR, for more information:
    <https://firebase.google.com/docs/cloud-messaging/migrate-v1>)
-   MAJOR UPDATES (AUGUST 2017):
    <https://github.com/olucurious/PyFCM/releases/tag/1.4.0>

Installation ==========

Install using pip:

    pip install pyfcm

    OR

    pip install git+https://github.com/olucurious/PyFCM.git

PyFCM supports Android, iOS and Web.

## Features

-   All FCM functionality covered
-   Tornado support

## Examples

### Send notifications using the `FCMNotification` class

``` python
# Send to single device.
from pyfcm import FCMNotification

fcm = FCMNotification(service_account_file="<service-account-json-path>", project_id="<project-id>")

# Google oauth2 credentials(such as ADC, impersonate credentials) can be used instead of service account file.

fcm = FCMNotification(
    service_account_file=None, credentials=your_credentials, project_id="<project-id>"
)

# OR initialize with proxies

proxy_dict = {
          "http"  : "http://127.0.0.1",
          "https" : "http://127.0.0.1",
        }
fcm = FCMNotification(service_account_file="<service-account-json-path>", project_id="<project-id>", proxy_dict=proxy_dict)

# OR using credentials from environment variable
# Often you would save service account json in evironment variable
# Assuming GCP_CREDENTIALS contains the data (TIP: use "export GCP_CREDENTIALS=$(filename.json)" to quickly load the json)

from google.oauth2 import service_account
gcp_json_credentials_dict = json.loads(os.getenv('GCP_CREDENTIALS', None))
credentials = service_account.Credentials.from_service_account_info(gcp_json_credentials_dict, scopes=['https://www.googleapis.com/auth/firebase.messaging'])
fcm = FCMNotification(service_account_file=None, credentials=credentials, project_id="<project-id>")

# Your service account file can be gotten from:  https://console.firebase.google.com/u/0/project/_/settings/serviceaccounts/adminsdk

# Now you are ready to send notification
fcm_token = "<fcm token>"
notification_title = "Uber update"
notification_body = "Hi John, your order is on the way!"
notification_image = "https://example.com/image.png"
result = fcm.notify(fcm_token=fcm_token, notification_title=notification_title, notification_body=notification_body, notification_image=notification_image)
print result
```

### Send a data message

``` python
# With FCM, you can send two types of messages to clients:
# 1. Notification messages, sometimes thought of as "display messages."
# 2. Data messages, which are handled by the client app.
# 3. Notification messages with optional data payload.

# Client app is responsible for processing data messages. Data messages have only custom key-value pairs. (Python dict)
# Data messages let developers send up to 4KB of custom key-value pairs.

# Sending a notification with data message payload
data_payload = {
    "foo": "bar",
    "body": "great match!",
    "room": "PortugalVSDenmark"
}
# To a single device
result = fcm.notify(fcm_token=fcm_token, notification_body=notification_body, data_payload=data_payload)

# Sending a data message only payload, do NOT include notification_body also do NOT include notification body
# To a single device
result = fcm.notify(fcm_token=fcm_token, data_payload=data_payload)

# Only string key and values are accepted. booleans, nested dicts are not supported
# To send nested dict, use something like
data_payload = {
    "foo": "bar",
    "data": json.dumps(data).
}
# For more info on format see https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#Message
# and https://firebase.google.com/docs/cloud-messaging/http-server-ref#downstream-http-messages-json

# Use notification messages when you want FCM to handle displaying a notification on your app's behalf.
# Use data messages when you just want to process the messages only in your app.
# PyFCM can send a message including both notification and data payloads.
# In such cases, FCM handles displaying the notification payload, and the client app handles the data payload.
```

### Appengine users should define their environment

``` python
fcm = FCMNotification(service_account_file="<service-account-json-path>", project_id="<project-id>", proxy_dict=proxy_dict, env='app_engine')
result = fcm.notify(fcm_token=fcm_token, notification_body=message)
```

### Sending a message to a topic

``` python
# Send a message to devices subscribed to a topic.
result = fcm.notify(topic_name="news", notification_body=message)

# Conditional topic messaging
topic_condition = "'TopicA' in topics && ('TopicB' in topics || 'TopicC' in topics)"
result = fcm.notify(notification_body=message, topic_condition=topic_condition)
# FCM first evaluates any conditions in parentheses, and then evaluates the expression from left to right.
# In the above expression, a user subscribed to any single topic does not receive the message. Likewise,
# a user who does not subscribe to TopicA does not receive the message. These combinations do receive it:
# TopicA and TopicB
# TopicA and TopicC
# Conditions for topics support two operators per expression, and parentheses are supported.
# For more information, check: https://firebase.google.com/docs/cloud-messaging/topic-messaging
```

### Extra argument options

-   android_config (dict, optional): Android specific options for messages -
        <https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#androidconfig>

-   apns_config (dict, optional): Apple Push Notification Service specific options -
        <https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#apnsconfig>

-   webpush_config (dict, optional): Webpush protocol options -
        <https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#webpushconfig>

-   fcm_options (dict, optional): Platform independent options for features provided by the FCM SDKs -
        <https://firebase.google.com/docs/reference/fcm/rest/v1/projects.messages#fcmoptions>
-  dry_run (bool, optional): If `True` no message will be sent but
        request will be tested.
