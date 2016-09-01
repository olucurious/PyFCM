from tornado import escape
from tornado import gen
from tornado.httpclient import AsyncHTTPClient, HTTPRequest

from ..baseapi import BaseAPI
from ..errors import AuthenticationError, InternalPackageError, FCMServerError
from ..fcm import FCMNotification


class TornadoBaseAPI(BaseAPI):
    def __init__(self, *args, **kwargs):
        super(TornadoBaseAPI, self).__init__(*args, **kwargs)
        self.http_client = AsyncHTTPClient()

    @gen.coroutine
    def send_request(self, payloads=None):
        for payload in payloads:
            request = HTTPRequest(
                url=self.FCM_END_POINT,
                method='POST',
                headers=self.request_headers(),
                body=payload
            )

            response = yield self.http_client.fetch(request)

            if response.code == 200:
                yield self.parse_response(response)
                return
            elif response.code == 401:
                raise AuthenticationError('There was an error authenticating the sender account')
            elif response.code == 400:
                raise InternalPackageError('Unknown internal error')
            else:
                raise FCMServerError('FCM server is temporarily unavailable')

    def parse_response(self, response):
        if 'content-length' in response.headers and int(response.headers['content-length']) <= 0:
            return {}

        parsed_response = escape.json_decode(response.body)

        multicast_id = parsed_response.get('multicast_id', None)
        success = parsed_response.get('success', 0)
        failure = parsed_response.get('failure', 0)
        canonical_ids = parsed_response.get('canonical_ids', 0)
        results = parsed_response.get('results', [])
        message_id = parsed_response.get('message_id', None)  # for topic messages
        if message_id:
            success = 1

        return {'multicast_id': multicast_id,
                'success': success,
                'failure': failure,
                'canonical_ids': canonical_ids,
                'results': results}


class TornadoFCMNotification(FCMNotification, TornadoBaseAPI):
    @gen.coroutine
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
                             title_loc_args=None):

        # [registration_id] cos we're sending to a single device
        payload = self.parse_payload(registration_ids=[registration_id],
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
                                     title_loc_args=title_loc_args)

        yield self.send_request([payload])
        return

    @gen.coroutine
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
                                title_loc_args=None):

        if len(registration_ids) > self.FCM_MAX_RECIPIENTS:
            payloads = list()
            registration_id_chunks = self.registration_id_chunks(registration_ids)
            for registration_ids in registration_id_chunks:
                # appends a payload with a chunk of registration ids here
                payloads.append(self.parse_payload(registration_ids=registration_ids,
                                                   message_body=message_body,
                                                   message_title=message_title,
                                                   sound=sound,
                                                   message_icon=message_icon,
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
                                                   title_loc_args=title_loc_args))
            yield self.send_request(payloads)
            return
        else:
            payload = self.parse_payload(registration_ids=registration_ids,
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
                                         title_loc_args=title_loc_args)
            yield self.send_request([payload])
            return

    @gen.coroutine
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
                                 title_loc_args=None):
        payload = self.parse_payload(topic_name=topic_name,
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
                                     title_loc_args=title_loc_args)
        yield self.send_request([payload])
        return
