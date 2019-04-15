from .baseapi import BaseAPI
from .errors import InvalidDataError


class FCMNotification(BaseAPI):
    def notify_single_device(self,
                             registration_id=None,
                             message_body=None,
                             message_title=None,
                             message_icon=None,
                             sound=None,
                             condition=None,
                             collapse_key=None,
                             delay_while_idle=False,
                             time_to_live=None,
                             restricted_package_name=None,
                             low_priority=False,
                             dry_run=False,
                             data_message=None,
                             click_action=None,
                             badge=None,
                             color=None,
                             tag=None,
                             body_loc_key=None,
                             body_loc_args=None,
                             title_loc_key=None,
                             title_loc_args=None,
                             content_available=None,
                             android_channel_id=None,
                             timeout=5,
                             extra_notification_kwargs=None,
                             extra_kwargs={}):
        """
        Send push notification to a single device

        Args:
            registration_id (list, optional): FCM device registration ID
            message_body (str, optional): Message string to display in the notification tray
            message_title (str, optional): Message title to display in the notification tray
            message_icon (str, optional): Icon that apperas next to the notification
            sound (str, optional): The sound file name to play. Specify "Default" for device default sound.
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            click_action (str, optional): Action associated with a user click on the notification
            badge (str, optional): Badge of notification
            color (str, optional): Color of the icon
            tag (str, optional): Group notification by tag
            body_loc_key (str, optional): Indicates the key to the body string for localization
            body_loc_args (list, optional): Indicates the string value to replace format
                specifiers in body string for localization
            title_loc_key (str, optional): Indicates the key to the title string for localization
            title_loc_args (list, optional): Indicates the string value to replace format
                specifiers in title string for localization
            content_available (bool, optional): Inactive client app is awoken
            android_channel_id (str, optional): Starting in Android 8.0 (API level 26),
                all notifications must be assigned to a channel. For each channel, you can set the
                visual and auditory behavior that is applied to all notifications in that channel.
                Then, users can change these settings and decide which notification channels from
                your app should be intrusive or visible at all.
            timeout (int, optional): set time limit for the request
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            extra_kwargs (dict, optional): More keyword arguments

        Returns:
            dict: Response from FCM server (`multicast_id`, `success`, `failure`, `canonical_ids`, `results`)

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided
                or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: Mostly from changes in the response of FCM,
                contact the project owner to resolve the issue
        """
        if registration_id is None:
            raise InvalidDataError('Invalid registration ID')
        # [registration_id] cos we're sending to a single device
        payload = self.parse_payload(
            registration_ids=[registration_id],
            message_body=message_body,
            message_title=message_title,
            message_icon=message_icon,
            sound=sound,
            condition=condition,
            collapse_key=collapse_key,
            delay_while_idle=delay_while_idle,
            time_to_live=time_to_live,
            restricted_package_name=restricted_package_name,
            low_priority=low_priority,
            dry_run=dry_run, data_message=data_message, click_action=click_action,
            badge=badge,
            color=color,
            tag=tag,
            body_loc_key=body_loc_key,
            body_loc_args=body_loc_args,
            title_loc_key=title_loc_key,
            title_loc_args=title_loc_args,
            android_channel_id=android_channel_id,
            content_available=content_available,
            extra_notification_kwargs=extra_notification_kwargs,
            **extra_kwargs
        )

        self.send_request([payload], timeout)
        return self.parse_responses()

    def single_device_data_message(self,
                                   registration_id=None,
                                   condition=None,
                                   collapse_key=None,
                                   delay_while_idle=False,
                                   time_to_live=None,
                                   restricted_package_name=None,
                                   low_priority=False,
                                   dry_run=False,
                                   data_message=None,
                                   content_available=None,
                                   android_channel_id=None,
                                   timeout=5,
                                   extra_notification_kwargs=None,
                                   extra_kwargs={}):
        """
        Send push message to a single device

        Args:
            registration_id (list, optional): FCM device registration ID
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            content_available (bool, optional): Inactive client app is awoken
            android_channel_id (str, optional): Starting in Android 8.0 (API level 26),
                all notifications must be assigned to a channel. For each channel, you can set the
                visual and auditory behavior that is applied to all notifications in that channel.
                Then, users can change these settings and decide which notification channels from
                your app should be intrusive or visible at all.
            timeout (int, optional): set time limit for the request
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            extra_kwargs (dict, optional): More keyword arguments

        Returns:
            dict: Response from FCM server (`multicast_id`, `success`, `failure`, `canonical_ids`, `results`)

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided
                or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: Mostly from changes in the response of FCM,
                contact the project owner to resolve the issue
        """
        if registration_id is None:
            raise InvalidDataError('Invalid registration ID')
        # [registration_id] cos we're sending to a single device
        payload = self.parse_payload(
            registration_ids=[registration_id],
            condition=condition,
            collapse_key=collapse_key,
            delay_while_idle=delay_while_idle,
            time_to_live=time_to_live,
            restricted_package_name=restricted_package_name,
            low_priority=low_priority,
            dry_run=dry_run,
            data_message=data_message,
            content_available=content_available,
            remove_notification=True,
            android_channel_id=android_channel_id,
            extra_notification_kwargs=extra_notification_kwargs,
            **extra_kwargs
        )

        self.send_request([payload], timeout)
        return self.parse_responses()

    def notify_multiple_devices(self,
                                registration_ids=None,
                                message_body=None,
                                message_title=None,
                                message_icon=None,
                                sound=None,
                                condition=None,
                                collapse_key=None,
                                delay_while_idle=False,
                                time_to_live=None,
                                restricted_package_name=None,
                                low_priority=False,
                                dry_run=False,
                                data_message=None,
                                click_action=None,
                                badge=None,
                                color=None,
                                tag=None,
                                body_loc_key=None,
                                body_loc_args=None,
                                title_loc_key=None,
                                title_loc_args=None,
                                content_available=None,
                                android_channel_id=None,
                                timeout=5,
                                extra_notification_kwargs=None,
                                extra_kwargs={}):
        """
        Sends push notification to multiple devices, can send to over 1000 devices

        Args:
            registration_ids (list, optional): FCM device registration IDs
            message_body (str, optional): Message string to display in the notification tray
            message_title (str, optional): Message title to display in the notification tray
            message_icon (str, optional): Icon that apperas next to the notification
            sound (str, optional): The sound file name to play. Specify "Default" for device default sound.
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            click_action (str, optional): Action associated with a user click on the notification
            badge (str, optional): Badge of notification
            color (str, optional): Color of the icon
            tag (str, optional): Group notification by tag
            body_loc_key (str, optional): Indicates the key to the body string for localization
            body_loc_args (list, optional): Indicates the string value to replace format
                specifiers in body string for localization
            title_loc_key (str, optional): Indicates the key to the title string for localization
            title_loc_args (list, optional): Indicates the string value to replace format
                specifiers in title string for localization
            content_available (bool, optional): Inactive client app is awoken
            android_channel_id (str, optional): Starting in Android 8.0 (API level 26),
                all notifications must be assigned to a channel. For each channel, you can set the
                visual and auditory behavior that is applied to all notifications in that channel.
                Then, users can change these settings and decide which notification channels from
                your app should be intrusive or visible at all.
            timeout (int, optional): set time limit for the request
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            extra_kwargs (dict, optional): More keyword arguments

        Returns:
            dict: Response from FCM server (`multicast_id`, `success`, `failure`, `canonical_ids`, `results`)

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided
                or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: JSON parsing error, mostly from changes in the response of FCM,
                create a new github issue to resolve it.
        """
        if not isinstance(registration_ids, list):
            raise InvalidDataError('Invalid registration IDs (should be list)')

        payloads = []

        registration_id_chunks = self.registration_id_chunks(registration_ids)
        for registration_ids in registration_id_chunks:
            # appends a payload with a chunk of registration ids here
            payloads.append(self.parse_payload(
                registration_ids=registration_ids,
                message_body=message_body,
                message_title=message_title,
                message_icon=message_icon,
                sound=sound,
                condition=condition,
                collapse_key=collapse_key,
                delay_while_idle=delay_while_idle,
                time_to_live=time_to_live,
                restricted_package_name=restricted_package_name,
                low_priority=low_priority,
                dry_run=dry_run, data_message=data_message,
                click_action=click_action,
                badge=badge,
                color=color,
                tag=tag,
                body_loc_key=body_loc_key,
                body_loc_args=body_loc_args,
                title_loc_key=title_loc_key,
                title_loc_args=title_loc_args,
                content_available=content_available,
                android_channel_id=android_channel_id,
                extra_notification_kwargs=extra_notification_kwargs,
                **extra_kwargs
            ))
        self.send_request(payloads, timeout)
        return self.parse_responses()

    def multiple_devices_data_message(self,
                                      registration_ids=None,
                                      condition=None,
                                      collapse_key=None,
                                      delay_while_idle=False,
                                      time_to_live=None,
                                      restricted_package_name=None,
                                      low_priority=False,
                                      dry_run=False,
                                      data_message=None,
                                      content_available=None,
                                      timeout=5,
                                      extra_notification_kwargs=None,
                                      extra_kwargs={}):
        """
        Sends push message to multiple devices, can send to over 1000 devices

        Args:
            registration_ids (list, optional): FCM device registration IDs
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            content_available (bool, optional): Inactive client app is awoken
            timeout (int, optional): set time limit for the request
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            extra_kwargs (dict, optional): More keyword arguments

        Returns:
            dict: Response from FCM server (`multicast_id`, `success`, `failure`, `canonical_ids`, `results`)

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided
                or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: JSON parsing error, mostly from changes in the response of FCM,
                create a new github issue to resolve it.
        """
        if not isinstance(registration_ids, list):
            raise InvalidDataError('Invalid registration IDs (should be list)')

        payloads = []
        registration_id_chunks = self.registration_id_chunks(registration_ids)
        for registration_ids in registration_id_chunks:
            # appends a payload with a chunk of registration ids here
            payloads.append(self.parse_payload(
                registration_ids=registration_ids,
                condition=condition,
                collapse_key=collapse_key,
                delay_while_idle=delay_while_idle,
                time_to_live=time_to_live,
                restricted_package_name=restricted_package_name,
                low_priority=low_priority,
                dry_run=dry_run,
                data_message=data_message,
                content_available=content_available,
                remove_notification=True,
                extra_notification_kwargs=extra_notification_kwargs,
                **extra_kwargs)
            )
        self.send_request(payloads, timeout)
        return self.parse_responses()

    def notify_topic_subscribers(self,
                                 topic_name=None,
                                 message_body=None,
                                 message_title=None,
                                 message_icon=None,
                                 sound=None,
                                 condition=None,
                                 collapse_key=None,
                                 delay_while_idle=False,
                                 time_to_live=None,
                                 restricted_package_name=None,
                                 low_priority=False,
                                 dry_run=False,
                                 data_message=None,
                                 click_action=None,
                                 badge=None,
                                 color=None,
                                 tag=None,
                                 body_loc_key=None,
                                 body_loc_args=None,
                                 title_loc_key=None,
                                 title_loc_args=None,
                                 content_available=None,
                                 android_channel_id=None,
                                 timeout=5,
                                 extra_notification_kwargs=None,
                                 extra_kwargs={}):
        """
        Sends push notification to multiple devices subscribed to a topic

        Args:
            topic_name (str, optional): Name of the topic to deliver messages to
            message_body (str, optional): Message string to display in the notification tray
            message_title (str, optional): Message title to display in the notification tray
            message_icon (str, optional): Icon that apperas next to the notification
            sound (str, optional): The sound file name to play. Specify "Default" for device default sound.
            condition (str, optiona): Topic condition to deliver messages to
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to `None`.
            delay_while_idle (bool, optional): deprecated
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to `None`
                which uses the FCM default of 4 weeks.
            restricted_package_name (str, optional): Name of package
            low_priority (bool, optional): Whether to send notification with
                the low priority flag. Defaults to `False`.
            dry_run (bool, optional): If `True` no message will be sent but request will be tested.
            data_message (dict, optional): Custom key-value pairs
            click_action (str, optional): Action associated with a user click on the notification
            badge (str, optional): Badge of notification
            color (str, optional): Color of the icon
            tag (str, optional): Group notification by tag
            body_loc_key (str, optional): Indicates the key to the body string for localization
            body_loc_args (list, optional): Indicates the string value to replace format
                specifiers in body string for localization
            title_loc_key (str, optional): Indicates the key to the title string for localization
            title_loc_args (list, optional): Indicates the string value to replace format
                specifiers in title string for localization
            content_available (bool, optional): Inactive client app is awoken
            android_channel_id (str, optional): Starting in Android 8.0 (API level 26),
                all notifications must be assigned to a channel. For each channel, you can set the
                visual and auditory behavior that is applied to all notifications in that channel.
                Then, users can change these settings and decide which notification channels from
                your app should be intrusive or visible at all.
            timeout (int, optional): set time limit for the request
            extra_notification_kwargs (dict, optional): More notification keyword arguments
            extra_kwargs (dict, optional): More keyword arguments

        Returns:
            dict: Response from FCM server (`multicast_id`, `success`, `failure`, `canonical_ids`, `results`)

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided
                or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: JSON parsing error, mostly from changes in the response of FCM,
                create a new github issue to resolve it.
        """
        payload = self.parse_payload(
            topic_name=topic_name,
            condition=condition,
            message_body=message_body,
            message_title=message_title,
            message_icon=message_icon,
            sound=sound,
            collapse_key=collapse_key,
            delay_while_idle=delay_while_idle,
            time_to_live=time_to_live,
            restricted_package_name=restricted_package_name,
            low_priority=low_priority,
            dry_run=dry_run, data_message=data_message, click_action=click_action,
            badge=badge,
            color=color,
            tag=tag,
            body_loc_key=body_loc_key,
            body_loc_args=body_loc_args,
            title_loc_key=title_loc_key,
            title_loc_args=title_loc_args,
            content_available=content_available,
            android_channel_id=android_channel_id,
            extra_notification_kwargs=extra_notification_kwargs,
            **extra_kwargs
        )
        self.send_request([payload], timeout)
        return self.parse_responses()
    
    def topic_subscribers_data_message(self,
                                       topic_name=None,
                                       condition=None,
                                       collapse_key=None,
                                       delay_while_idle=False,
                                       time_to_live=None,
                                       restricted_package_name=None,
                                       low_priority=False,
                                       dry_run=False,
                                       data_message=None,
                                       content_available=None,
                                       timeout=5,
                                       extra_notification_kwargs=None,
                                       extra_kwargs={}):                                 
        """
        Sends data notification to multiple devices subscribed to a topic
        Args:
            topic_name (topic_name): Name of the topic to deliver messages to
            condition (condition): Topic condition to deliver messages to
            A topic name is a string that can be formed with any character in [a-zA-Z0-9-_.~%]
            data_message (dict): Data message payload to send alone or with the notification message
            
        Keyword Args:
            collapse_key (str, optional): Identifier for a group of messages
                that can be collapsed so that only the last message gets sent
                when delivery can be resumed. Defaults to ``None``.
            delay_while_idle (bool, optional): If ``True`` indicates that the
                message should not be sent until the device becomes active.
            time_to_live (int, optional): How long (in seconds) the message
                should be kept in FCM storage if the device is offline. The
                maximum time to live supported is 4 weeks. Defaults to ``None``
                which uses the FCM default of 4 weeks.
            low_priority (boolean, optional): Whether to send notification with
                the low priority flag. Defaults to ``False``.
            restricted_package_name (str, optional): Package name of the
                application where the registration IDs must match in order to
                receive the message. Defaults to ``None``.
            dry_run (bool, optional): If ``True`` no message will be sent but
                request will be tested.
            
        Returns:
            :tuple:`multicast_id(long), success(int), failure(int), canonical_ids(int), results(list)`:
            Response from FCM server.
        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: JSON parsing error, mostly from changes in the response of FCM, create a new github issue to resolve it.
        """
        if extra_kwargs is None:
            extra_kwargs = {}
        payload = self.parse_payload(topic_name=topic_name,
                                     condition=condition,
                                     collapse_key=collapse_key,
                                     delay_while_idle=delay_while_idle,
                                     time_to_live=time_to_live,
                                     restricted_package_name=restricted_package_name,
                                     low_priority=low_priority,
                                     dry_run=dry_run,
                                     data_message=data_message,
                                     content_available=content_available,
                                     remove_notification=True,
                                     extra_notification_kwargs=extra_notification_kwargs,
                                     **extra_kwargs)
        self.send_request([payload], timeout)
        return self.parse_responses()
