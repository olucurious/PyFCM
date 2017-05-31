from .baseapi import BaseAPI
from .errors import *


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
                             extra_kwargs={}):

        """
        Send push notification to a single device

        Args:
            registration_id (str): FCM device registration IDs.
            message_body (str): Message string to display in the notification tray
            data_message (dict): Data message payload to send alone or with the notification message
            sound (str): The sound file name to play. Specify "Default" for device default sound.

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
            :dict:`multicast_id(long), success(int), failure(int), canonical_ids(int), results(list)`:
            Response from FCM server.

        Raises:
            AuthenticationError: If :attr:`api_key` is not set or provided or there is an error authenticating the sender.
            FCMServerError: Internal server error or timeout error on Firebase cloud messaging server
            InvalidDataError: Invalid data provided
            InternalPackageError: Mostly from changes in the response of FCM, contact the project owner to resolve the issue
        """
        if registration_id is None:
            raise InvalidDataError('Invalid registration ID')
        # [registration_id] cos we're sending to a single device
        payload = self.parse_payload(registration_ids=[registration_id],
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
                                     content_available=content_available,
                                     **extra_kwargs)

        self.send_request([payload])
        return self.parse_responses()[-1:][0]

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
                                extra_kwargs={}):

        """
        Sends push notification to multiple devices,
        can send to over 1000 devices

        Args:
            registration_ids (list): FCM device registration IDs.
            message_body (str): Message string to display in the notification tray
            data_message (dict): Data message payload to send alone or with the notification message
            sound (str): The sound file name to play. Specify "Default" for device default sound.

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
        if len(registration_ids) > self.FCM_MAX_RECIPIENTS:
            payloads = list()
            registration_id_chunks = self.registration_id_chunks(registration_ids)
            for registration_ids in registration_id_chunks:
                # appends a payload with a chunk of registration ids here
                payloads.append(self.parse_payload(registration_ids=registration_ids,
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
                                                   **extra_kwargs))
            self.send_request(payloads)
            return self.parse_responses()
        else:
            payload = self.parse_payload(registration_ids=registration_ids,
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
                                         content_available=content_available,
                                         **extra_kwargs)
            self.send_request([payload])
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
                                 extra_kwargs={}):

        """
        Sends push notification to multiple devices subscribe to a topic

        Args:
            topic_name (topic_name): Name of the topic to deliver messages to
            condition (condition): Topic condition to deliver messages to
            A topic name is a string that can be formed with any character in [a-zA-Z0-9-_.~%]
            message_body (str): Message string to display in the notification tray
            data_message (dict): Data message payload to send alone or with the notification message
            sound (str): The sound file name to play. Specify "Default" for device default sound.

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
        payload = self.parse_payload(topic_name=topic_name,
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
                                     **extra_kwargs)
        self.send_request([payload])
        return self.parse_responses()[-1:][0]
