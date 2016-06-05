from baseapi import BaseAPI

class FCMNotification(BaseAPI):

    def notify_single_device(self,
                 registration_id,
                 message_body,
                 message_title=None,
                 message_icon=None,
                 notification=None,
                 collapse_key=None,
                 delay_while_idle=False,
                 time_to_live=None,
                 restricted_package_name=None,
                 low_priority=False,
                 dry_run=False,
                 extra_data=None):
        """
        Send push notification to a single device

        Args:
            registration_id (str): FCM device registration IDs.
            message_body (str): Message string to display in the notification tray

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
        payload = self.parse_payload(registration_id, message_body, message_title, message_icon, notification,collapse_key,
                 delay_while_idle, time_to_live,restricted_package_name, low_priority, dry_run, extra_data)
        return self.send_request([payload])

    def notify_multiple_devices(self,
                 registration_ids,
                 message_body,
                 message_title=None,
                 message_icon=None,
                 notification=None,
                 collapse_key=None,
                 delay_while_idle=False,
                 time_to_live=None,
                 restricted_package_name=None,
                 low_priority=False,
                 dry_run=False,
                 extra_data=None):
        """
        Sends push notification to multiple devices,
        can send to over 1000 devices

        Args:
            registration_ids (list): FCM device registration IDs.
            message_body (str): Message string to display in the notification tray

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
                payloads.append(self.parse_payload(registration_ids, message_body, message_title, message_icon, notification,collapse_key,
                         delay_while_idle, time_to_live,restricted_package_name, low_priority, dry_run, extra_data))
            return self.send_request(payloads)
        else:
            payload = self.parse_payload(registration_ids, message_body, message_title, message_icon, notification,collapse_key,
                     delay_while_idle, time_to_live,restricted_package_name, low_priority, dry_run, extra_data)
            return self.send_request([payload])

