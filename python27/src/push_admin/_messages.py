# -*-coding:utf-8-*-
#
# Copyright 2020. Huawei Technologies Co., Ltd. All rights reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import numbers
import re
import six


class Message(object):
    """A message that can be sent Huawei Cloud Messaging.

    Args:
        data: A string value.
        notification: An instance of ``messaging.Notification`` (optional).
        android: An instance of ``messaging.Android`` (optional).
        apns: APSN related message definition
        web_push: Web Push related message definition
        token: token list, must be tuple (optional).
        topic: message topic, must be string (optional).
        condition: message condition, must be string (optional).
    """
    def __init__(self, data=None, notification=None, android=None, apns=None, web_push=None, token=None,
                 topic=None, condition=None):
        MessageValidator.check_message(data, notification, android, apns, web_push, token, topic, condition)
        self.data = data
        self.notification = notification
        self.android = android
        self.apns = apns
        self.web_push = web_push
        self.token = token
        self.topic = topic
        self.condition = condition


class Notification(object):
    """A notification that can be included in a message.

    Args:
        title: Title of the notification (optional).
        body: Body of the notification (optional).
    """
    def __init__(self, title=None, body=None, image=None):
        MessageValidator.check_notification(title, body, image)
        self.title = title
        self.body = body
        self.image = image


# ----------------------------------------------------------------------------------------------------------------------


class APNsConfig(object):
    """
    Please refer to the Apple APNS API reference:
    https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual/RemoteNotificationsPG/\
    CommunicatingwithAPNs.html
    """
    def __init__(self, headers=None, payload=None, apns_hms_options=None):
        MessageValidator.check_apns_config(headers=headers, payload=payload, apns_hms_options=apns_hms_options)
        self.headers = headers
        self.payload = payload
        self.apns_hms_options = apns_hms_options


class APNsHeader(object):
    """
    authorization
    apns-id
    apns-expiration
    apns-priority
    apns-topic
    apns-collapse-id
    """
    HEAD_AUTHORIZATION = "authorization"
    HEAD_APNs_ID = "apns-id"
    HEAD_APNs_EXPIRATION = "apns-expiration"
    HEAD_APNs_PRIORITY = "apns-priority"
    HEAD_APNs_TOPIC = "pns-topic"
    HEAD_APNs_COLLAPSE_ID = "apns-collapse-id"


class APNsPayload(object):
    """
     APNs payload definition
    """
    def __init__(self, aps, **kwargs):
        MessageValidator.check_apns_payload(aps=aps)
        self.aps = aps
        self.custom_data = kwargs


class APNsAps(object):
    """
    APNs aps definition: https://developer.apple.com/library/archive/documentation/NetworkingInternet/Conceptual\
                        /RemoteNotificationsPG/PayloadKeyReference.html#//apple_ref/doc/uid/TP40008194-CH17-SW1

    one sample is as follows:

    {
        "aps" : {
            "alert" : {
                "title" : "Game Request",
                "body" : "Bob wants to play poker",
                "action-loc-key" : "PLAY"
                "loc-key" : "GAME_PLAY_REQUEST_FORMAT",
                "loc-args" : [ "Jenna", "Frank"],
                "content-available" : 1
            },
            "badge" : 5,
            "sound" : "bingbong.aiff",
        },
        "acme1" : "bar",
        "acme2" : [ "bang",  "whiz" ]
    }
    """
    def __init__(self, alert=None, badge=None, sound=None, content_available=None, category=None,
                 thread_id=None, mutable_content=None, custom_data=None):
        MessageValidator.check_apns_payload_aps(alert=alert, badge=badge, sound=sound,
                                                content_available=content_available, category=category,
                                                thread_id=thread_id, mutable_content=mutable_content,
                                                custom_data=custom_data)
        self.alert = alert
        self.badge = badge
        self.sound = sound
        self.content_available = content_available
        self.category = category
        self.thread_id = thread_id
        self.mutable_content = mutable_content
        self.custom_data = custom_data


class APNsAlert(object):
    """An alert that can be included in ``messaging.Aps``.

    Args:

    """

    def __init__(self, title=None, body=None, loc_key=None, loc_args=None,
                 title_loc_key=None, title_loc_args=None, action_loc_key=None, launch_image=None,
                 custom_data=None):
        MessageValidator.check_apns_payload_aps_alert(title=title, body=body, loc_key=loc_key, loc_args=loc_args,
                                                      title_loc_key=title_loc_key, title_loc_args=title_loc_args,
                                                      action_loc_key=action_loc_key, launch_image=launch_image,
                                                      custom_data=custom_data)
        self.title = title
        self.body = body
        self.loc_key = loc_key
        self.loc_args = loc_args
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.action_loc_key = action_loc_key
        self.launch_image = launch_image
        self.custom_data = custom_data


class APNsHMSOptions(object):
    """Options for features provided by the FCM SDK for iOS.

    Args:
        target_user_type: Developer or Commercial enviroment
    """
    def __init__(self, target_user_type=None):
        MessageValidator.check_apns_hms_options(target_user_type=target_user_type)
        self.target_user_type = target_user_type


# ----------------------------------------------------------------------------------------------------------------------


class WebPushConfig(object):
    """
        Web push-specific options that can be included in a message.
        For Web Push Specification Reference: https://tools.ietf.org/html/rfc8030#section-5
        For mozilla implementation: https://developer.mozilla.org/en-US/docs/Web/API/notification
    """
    TTL_HEADER = "ttl"
    URGENCY_HEADER = "urgency"
    TOPIC_HEADER = "topic"

    def __init__(self, headers=None, data=None, notification=None, hms_options=None):
        """

        :param headers: A dictionary of headers (optional). Refer `Web push Specification`_ for supported headers.
        :param notification:  A ``messaging.WebPushNotification`` to be included in the message (optional).
        :param hms_options:  A ``WebPushHMSOptions`` instance to be included in the message(optional).
        """
        MessageValidator.check_webpush_config(headers, data, notification, hms_options)
        """ Refer to https://tools.ietf.org/html/rfc7240 """
        self.headers = headers
        """ message deliver to the end application directly """
        self.data = data
        """ Refer to  WebPushNotification """
        self.notification = notification
        """ Refer to WebPushHMSOptions"""
        self.hms_options = hms_options


class WebPushHeader(object):
    """
     Web Push Header, refer to: https://tools.ietf.org/html/rfc7240
    """
    def __init__(self, ttl=None, urgency=None, topic=None):
        MessageValidator.check_webpush_header(ttl, urgency, topic)
        self.ttl = ttl
        self.urgency = urgency
        self.topic = topic


class WebPushNotification(object):
    """
     Web Push Notification
    """
    def __init__(self, title=None, body=None, icon=None, actions=None, badge=None, data=None, dir=None,
                 image=None, lang=None, renotify=None, require_interaction=None, silent=None, tag=None,
                 timestamp=None, vibrate=None):
        MessageValidator.check_webpush_notification(title=title, body=body, icon=icon, actions=actions, badge=badge,
                                                    data=data, dir=dir, image=image, lang=lang,
                                                    renotify=renotify, require_interaction=require_interaction,
                                                    silent=silent, tag=tag, timestamp=timestamp, vibrate=vibrate)
        self.title = title
        self.body = body
        """ Refer to WebPushNotificationAction """
        self.actions = actions
        self.badge = badge
        self.data = data
        self.dir = dir
        self.icon = icon
        self.image = image
        self.lang = lang
        self.renotify = renotify
        self.require_interaction = require_interaction
        self.silent = silent
        self.tag = tag
        self.timestamp = timestamp
        self.vibrate = vibrate


class WebPushNotificationAction(object):
    """
    The action for web push notification
    """
    def __init__(self, action=None, title=None, icon=None):
        """

        :param action:
        :param title:
        :param icon:
        """
        MessageValidator.check_webpush_notification_action(action=action, title=title, icon=icon)
        self.action = action
        self.icon = icon
        self.title = title


class WebPushHMSOptions(object):
    """
    optional link option
    """
    def __init__(self, link=None):
        MessageValidator.check_webpush_hms_options(link)
        self.link = link


# ----------------------------------------------------------------------------------------------------------------------


class AndroidConfig(object):

    HIGH_PRIORITY = "HIGH"
    NORMAL_PRIORITY = "NORMAL"

    """
    Android-specific options that can be included in a message.
    """
    def __init__(self, collapse_key=None, urgency='NORMAL', ttl=None, bi_tag=None
                 , fast_app_target=None, notification=None, data=None, category=None):
        MessageValidator.check_android_config(collapse_key, urgency, ttl, bi_tag, fast_app_target
                                              , notification, data)
        self.collapse_key = collapse_key
        self.urgency = urgency
        self.ttl = ttl
        self.bi_tag = bi_tag
        self.fast_app_target = fast_app_target
        self.notification = notification
        self.data = data
        self.category = category


class AndroidNotification(object):

    PRIORITY_LOW = "LOW"
    PRIORITY_DEFAULT = "NORMAL"
    PRIORITY_HIGH = "HIGH"


    VISIBILITY_UNSPECIFIED = "VISIBILITY_UNSPECIFIED"
    PRIVATE = "PRIVATE"
    PUBLIC = "PUBLIC"
    SECRET = "SECRET"

    """
    Android-specific notification parameters.
    """

    def __init__(self, title=None, body=None, icon=None, color=None, sound=None, default_sound=None, tag=None,
                 click_action=None, body_loc_key=None, body_loc_args=None, title_loc_key=None,
                 title_loc_args=None, multi_lang_key=None, channel_id=None, notify_summary=None, image=None,
                 style=None, big_title=None, big_body=None, auto_clear=None, notify_id=None, group=None, badge=None,
                 ticker=None, auto_cancel=None, when=None, importance=None, use_default_vibrate=True,
                 use_default_light=True, vibrate_config=None, visibility=None, light_settings=None, foreground_show=False):

        MessageValidator.check_android(title=title, body=body, icon=icon, color=color, sound=sound,
                                       default_sound=default_sound, tag=tag, click_action=click_action,
                                       body_loc_key=body_loc_key, body_loc_args=body_loc_args,
                                       title_loc_key=title_loc_key, title_loc_args=title_loc_args,
                                       multi_lang_key=multi_lang_key, channel_id=channel_id,
                                       notify_summary=notify_summary,
                                       image=image, style=style, big_title=big_title, big_body=big_body,
                                       auto_clear=auto_clear, notify_id=notify_id,
                                       group=group, badge=badge, ticker=ticker, auto_cancel=auto_cancel, when=when,
                                       importance=importance,
                                       use_default_vibrate=use_default_vibrate,
                                       use_default_light=use_default_light, vibrate_config=vibrate_config,
                                       visibility=visibility, light_settings=light_settings,
                                       foreground_show=foreground_show)
        self.title = title
        self.body = body
        self.icon = icon
        self.color = color
        self.sound = sound
        self.default_sound = default_sound
        self.tag = tag
        self.click_action = click_action
        self.body_loc_key = body_loc_key
        self.body_loc_args = body_loc_args
        self.title_loc_key = title_loc_key
        self.title_loc_args = title_loc_args
        self.multi_lang_key = multi_lang_key
        self.channel_id = channel_id
        self.notify_summary = notify_summary
        self.image = image
        self.style = style
        self.big_title = big_title
        self.big_body = big_body
        self.auto_clear = auto_clear
        self.notify_id = notify_id
        self.group = group
        self.badge = badge
        self.ticker = ticker
        self.auto_cancel = auto_cancel
        self.when = when
        self.importance = importance
        self.use_default_vibrate = use_default_vibrate
        self.use_default_light = use_default_light
        self.vibrate_config = vibrate_config
        self.visibility = visibility
        self.light_settings = light_settings
        self.foreground_show = foreground_show


class AndroidClickAction(object):
    """A ClickAction that can be included in a message.android.notification.

    Args:
        action_type: type of the android.notification (optional).
        intent: intent of the android.notification (optional).
        url: url of the android.notification (optional).
        action: action definition for push message
        rich_resource: rich_resource of the android.notification (optional).
    """
    def __init__(self, action_type=None, intent=None, action=None, url=None, rich_resource=None):
        MessageValidator.check_click_action(action_type=action_type, intent=intent, action=action, url=url,
                                            rich_resource=rich_resource)
        self.action_type = action_type
        self.intent = intent
        self.action = action
        self.url = url
        self.rich_resource = rich_resource


class AndroidBadgeNotification(object):
    """A BadgeNotification that can be included in a message.android.notification.

    Args:
        add_num: message number of badge notification in the android.notification (optional).
        set_num: set the specific number of badge notification (optional).
        clazz: message class of badge notification in the android.notification (optional).
    """
    def __init__(self, add_num=None, set_num=None, clazz=None):
        MessageValidator.check_badge_notification(add_num=add_num, set_num=set_num, clazz=clazz)
        self.add_num = add_num
        self.set_num = set_num
        self.clazz = clazz


class AndroidLightSettings(object):
    """
        light_settings":{
            "color":{
                "alpha":0,
                "red":0,
                "green":1,
                "blue":1
            },
            "light_on_duration":"3.5",
            "light_off_duration":"5S"
        }
    """
    def __init__(self, color=None, light_on_duration=None, light_off_duration=None):
        MessageValidator.check_light_settings(color=color, light_on_duration=light_on_duration, light_off_duration=light_off_duration)
        self.color = color
        self.light_on_duration = light_on_duration
        self.light_off_duration = light_off_duration


class AndroidLightSettingsColor(object):
    """
        "color":{
                "alpha":0,
                "red":0,
                "green":1,
                "blue":1
            }
    """
    def __init__(self, alpha=None, red=None, green=None, blue=None):
        MessageValidator.check_light_settings_color(alpha=alpha, red=red, green=green, blue=blue)
        self.alpha = alpha
        self.red = red
        self.green = green
        self.blue = blue

# --------------------------------------------------------------------------------------------------------------------


class MessageValidator(object):
    """
        message validation utilities.
        Methods provided in this class raise ValueErrors if any validations fail.
    """
    @classmethod
    def check_https_url(cls, hint, value):
        cls.check_string(hint, value)
        if value is not None and not re.match(r"^https:/{2}\w.+$", value):
            raise ValueError('{0} must be a valid https url.'.format(hint))

    @classmethod
    def check_string(cls, hint, value, non_empty=False):
        """Checks if the given value is a string."""
        if value is None:
            return None
        if not isinstance(value, six.string_types):
            if non_empty:
                raise ValueError('{0} must be a non-empty string.'.format(hint))
            else:
                raise ValueError('{0} must be a string.'.format(hint))
        if non_empty and not value:
            raise ValueError('{0} must be a non-empty string.'.format(hint))
        return value

    @classmethod
    def assert_string_values(cls, hint, value, *args):
        """
        Check the class value should be an instance of string, and related values should be within *args
        :param hint: prompt message
        :param value: the real value
        :param args: the specific value list
        :return:
        """
        if value is None:
            return None
        if not isinstance(value, six.string_types):
                raise ValueError('{0} must be a string.'.format(hint))
        for v in args:
            if value.__eq__(v):
                return value

        raise ValueError('{} must be a value within{}.'.format(hint, args))

    @classmethod
    def check_string_list(cls, label, value):
        """Checks if the given value is a list comprised only of strings."""
        if value is None or value == []:
            return None
        if not isinstance(value, list):
            raise ValueError('{0} must be a list of strings.'.format(label))
        non_str = [k for k in value if not isinstance(k, six.string_types)]
        if non_str:
            raise ValueError('{0} must not contain non-string values.'.format(label))
        return value

    @classmethod
    def check_boolean(cls, hint, value):
        """Checks if the given value is a string."""
        if value is None:
            return None
        if not isinstance(value, bool):
            raise ValueError('{0} must be a boolean.'.format(hint))
        return value

    @classmethod
    def count_boolean(cls, *args):
        count = 0
        for v in args:
            if v:
                count += 1
        return count

    @classmethod
    def check_not_all_none(cls, hint, *args):
        total_size = len(args)
        count = 0
        for data in args:
            if data is None:
                count += 1
        if total_size == count:
            raise ValueError(hint)

    @classmethod
    def check_type(cls, class_obj, class_type, hint):
        if (class_obj is not None) and (not isinstance(class_obj, class_type)):
            raise ValueError(hint)

    @classmethod
    def check_type_list(cls, label, value, cls_type):
        """Checks if the given value is a list comprised only of numbers."""
        if value is None or value == []:
            return None
        if not isinstance(value, list):
            raise ValueError('{0} must be a list of {1}.'.format(label, cls_type))
        non_number = [k for k in value if not isinstance(k, cls_type)]
        if non_number:
            raise ValueError('{0} must not contain non-{1} values.'.format(label, cls_type))
        return value

    @classmethod
    def check_number(cls, label, value):
        if value is None:
            return None
        if not isinstance(value, numbers.Number):
            raise ValueError('{0} must be a number.'.format(label))
        return value

    @classmethod
    def check_number_span(cls, label, value, min, max):
        if value is None:
            return None
        if not isinstance(value, numbers.Number):
            raise ValueError('{0} must be a number.'.format(label))
        if value < min or value > max:
            raise ValueError('{0} must be within {1} to {2}.'.format(label, min, max))
        return value

    @classmethod
    def assert_integer_values(cls, hint, value, *args):
        """
        Check the class value should be an instance of string, and related values should be within *args
        :param hint: prompt message
        :param value: the real value
        :param args: the specific value list
        :return:
        """
        if value is None:
            return None
        if not isinstance(value, six.integer_types):
            raise ValueError('{0} must be a integer.'.format(hint))
        for v in args:
            if value == v:
                return value

        raise ValueError('{} must be a value within{}.'.format(hint, args))

    @classmethod
    def check_number_list(cls, label, value):
        if value is None or value == []:
            return None
        if not isinstance(value, list):
            raise ValueError('{0} must be a list of numbers.'.format(label))
        non_number = [k for k in value if not isinstance(k, numbers.Number)]
        if non_number:
            raise ValueError('{0} must not contain non-number values.'.format(label))
        return value

    @classmethod
    def check_string_dict(cls, label, value):
        if value is None or value == {}:
            return None
        if not isinstance(value, dict):
            raise ValueError('{0} must be a dictionary.'.format(label))
        non_str = [k for k in value if not isinstance(k, six.string_types)]
        if non_str:
            raise ValueError('{0} must not contain non-string keys.'.format(label))
        return value

    # ------------------------------------------------------------------------------------------------------------------

    @classmethod
    def check_message(cls, data, notification, android, apns, web_push, token, topic, condition):
        """
        Check whether the message parameter is valid or not

        :param data:
        :param notification:
        :param android:
        :param apns:
        :param web_push:
        :param token:
        :param topic:
        :param condition:
        :return:
        """
        # data must be string
        cls.check_string(hint="Message.data", value=data)

        # notification
        if (notification is not None) and (not isinstance(notification, Notification)):
            raise ValueError('notification must be an instance of Notification class')

        # android / APNs / Web Push
        # if notification message(data is None), one of android / APNs / Web Push must be present
        if data is None:
            cls.check_not_all_none('Message.data is None, one of Message.android/Message.apns/Message.webpush \
            must be present', android, apns, web_push)

        cls.check_type(android, AndroidConfig, 'android must be an instance of AndroidConfig class')
        cls.check_type(apns, APNsConfig, 'apns must be an instance of APNsConfig class')
        cls.check_type(web_push, WebPushConfig, 'web_push must be an instance of WebPushConfig class')

        """token, topic, condition"""
        # [token, topic, condition] only one not None
        target_count = cls.count_boolean(token is not None, topic is not None, condition is not None)
        if target_count != 1:
            raise ValueError('Exactly one of token, topic or condition must be specified.')

        # token must be tuple or list
        if token is not None:
            if not isinstance(token, tuple) and not isinstance(token, list):
                raise ValueError('token must be a tuple or a list')
            if len(token) > 1000:
                raise ValueError('token must not contain more than 1000 tokens')

        cls.check_string(hint="Message.topic", value=topic)
        cls.check_string(hint="Message.condition", value=condition)

    @classmethod
    def check_notification(cls, title, body, image):
        cls.check_string(hint="Notification.title", value=title)
        cls.check_string(hint="Notification.body", value=body)
        cls.check_https_url(hint="Notification.image", value=image)

    @classmethod
    def check_android_config(cls, collapse_key, urgency, ttl, bi_tag, fast_app_target, notification, data):
        # collapse_key
        cls.check_number('AndroidConfig.collapse_key', collapse_key)
        # urgency
        cls.assert_string_values("AndroidConfig.urgency", urgency, AndroidConfig.HIGH_PRIORITY,
                                 AndroidConfig.NORMAL_PRIORITY)
        # ttl
        cls.check_string(hint="AndroidConfig.ttl", value=ttl)
        # bi_tag
        cls.check_string(hint="AndroidConfig.bi_tag", value=bi_tag)
        # fast_app_target
        cls.check_number_span("AndroidConfig.fast_app_target", fast_app_target, 1, 2)
        # notification
        cls.check_type(notification, AndroidNotification,
                       hint='notification must be an instance of AndroidNotification')
        # data
        cls.check_string(hint="AndroidConfig.data", value=data)

    @classmethod
    def check_android(cls, title, body, icon, color, sound, default_sound, tag, click_action, body_loc_key, body_loc_args,
                      title_loc_key, title_loc_args, multi_lang_key, channel_id, notify_summary, image,
                      style, big_title, big_body, auto_clear, notify_id, group, badge,
                      ticker, auto_cancel, when, importance,
                      use_default_vibrate, use_default_light, vibrate_config, visibility, light_settings,
                      foreground_show):
        # title
        cls.check_string(hint="AndroidNotification.title", value=title)
        # body
        cls.check_string(hint="AndroidNotification.body", value=body)
        # icon
        cls.check_string(hint="AndroidNotification.icon", value=icon)
        # color
        cls.check_string(hint="AndroidNotification.color", value=color)
        # sound
        cls.check_string(hint="AndroidNotification.sound", value=sound)
        # default_sound
        cls.check_boolean(hint="AndroidNotification.default_sound", value=default_sound)
        # tag
        cls.check_string(hint="AndroidNotification.tag", value=tag)
        # click_action
        cls.check_type(click_action, AndroidClickAction,
                       hint='click_action must be an instance of AndroidClickAction')
        # body_loc_key
        cls.check_string(hint="AndroidNotification.body_loc_key", value=body_loc_key)
        # body_loc_args
        if (body_loc_args is not None) and (not isinstance(body_loc_args, tuple)) and (not isinstance(body_loc_args, list)):
            raise ValueError('AndroidNotification.body_loc_args must be an instance of tuple or list')
        # title_loc_key
        cls.check_string(hint="AndroidNotification.title_loc_key", value=title_loc_key)
        # title_loc_args
        if (title_loc_args is not None) and (not isinstance(title_loc_args, tuple) and not isinstance(title_loc_args, list)):
            raise ValueError('AndroidNotification.title_loc_args must be an instance of tuple or list')
        # multi_lang_key
        if multi_lang_key is not None:
            if not isinstance(multi_lang_key, dict):
                raise ValueError('AndroidNotification.multi_lang_key must be a dict.')
        # channel_id
        cls.check_string(hint="AndroidNotification.channel_id", value=channel_id)
        # notify_summary
        cls.check_string(hint="AndroidNotification.notify_summary", value=notify_summary)
        #
        # image
        cls.check_https_url(hint="AndroidNotification.image", value=image)
        # style
        if style is not None:
            if style not in [0, 1, 2]:
                raise ValueError('AndroidNotification.style must in [0, 1, 2]')
            # big_title, big_body
            if style == 1:
                if (big_title is None) or (not isinstance(big_title, str)):
                    raise ValueError('AndroidNotification.big_title must be valid string when style is 1')
                if (big_body is None) and (not isinstance(big_body, str)):
                    raise ValueError('AndroidNotification.big_body must be valid string when style is 1')
            # # big_picture
            # if style == 2:
            #     if (big_picture is None) or (not isinstance(big_picture, str)):
            #         raise ValueError('AndroidNotification.big_picture must be valid string when style is 2')
            #     if not big_picture.upper().startswith('HTTPS'):
            #         raise ValueError('AndroidNotification.big_picture must be valid https url address when type is 2')
        # auto_clear
        cls.check_number(label='AndroidNotification.auto_clear ', value=auto_clear)
        # notify_id
        cls.check_number(label='AndroidNotification.notify_id ', value=notify_id)
        # group
        cls.check_string(hint="AndroidNotification.group", value=group)
        # badge
        cls.check_type(badge, AndroidBadgeNotification, "badge should be an instance of AndroidBadgeNotification")
        # ticker
        cls.check_string(hint="AndroidNotification.ticker", value=ticker)
        # auto_cancel
        cls.check_boolean(hint="AndroidNotification.auto_cancel", value=auto_cancel)
        # when
        cls.check_string(hint="AndroidNotification.when", value=when)
        # importance
        cls.assert_string_values("AndroidNotification.importance", importance,
                                 AndroidNotification.PRIORITY_DEFAULT,
                                 AndroidNotification.PRIORITY_HIGH, AndroidNotification.PRIORITY_LOW)
        # use_default_vibrate
        cls.check_boolean(hint="AndroidNotification.use_default_vibrate", value=use_default_vibrate)
        # use_default_light
        cls.check_boolean(hint="AndroidNotification.use_default_light", value=use_default_light)
        # vibrate_config
        cls.check_string_list(label="AndroidNotification.vibrate_config", value=vibrate_config)
        # visibility
        cls.assert_string_values("AndroidNotification.visibility", visibility,
                                 AndroidNotification.PRIVATE,
                                 AndroidNotification.PUBLIC, AndroidNotification.SECRET,
                                 AndroidNotification.VISIBILITY_UNSPECIFIED)
        # light_settings
        cls.check_type(light_settings, AndroidLightSettings, "light_settings should be an instance of AndroidLightSettings")
        # foreground_show
        cls.check_boolean(hint="AndroidNotification.foreground_show", value=foreground_show)

    @classmethod
    def check_badge_notification(cls, add_num, set_num, clazz):
        # add_num must be int
        cls.check_number_span(label="AndroidBadgeNotification.add_num", value=add_num, min=0, max=100)
        # set_num must be int
        cls.check_number_span(label="AndroidBadgeNotification.set_num", value=set_num, min=0, max=100)
        # clazz
        cls.check_string(hint="AndroidBadgeNotification.clazz", value=clazz)

    @classmethod
    def check_click_action(cls, action_type, intent, action, url, rich_resource):
        # type must be in [1, 4]
        if (action_type is None) or (action_type not in [1, 2, 3, 4]):
            raise ValueError('ClickAction.type must be in [1, 2, 3, 4]')

        # intent, if type is 1, intent or action must be present or both
        if action_type == 1:
            count = cls.count_boolean(isinstance(intent, str), isinstance(action, str))
            if count <= 0:
                raise ValueError('ClickAction.intent or ClickAction.action must be present or both when click_type is 1')

        # url, if type is 2, url must
        if action_type == 2:
            if not isinstance(url, str):
                raise ValueError('ClickAction.url must when ClickAction.type is 2')
            if not url.upper().startswith('HTTPS'):
                raise ValueError('ClickAction.url must be https prefix when ClickAction.type is 2')

        # rich_resource, if type is 4, rich_resource must
        if action_type == 4:
            if not isinstance(rich_resource, str):
                raise ValueError('ClickAction.rich_resource must when ClickAction.type is 4')
            if not rich_resource.upper().startswith('HTTPS'):
                raise ValueError('ClickAction.rich_resource must be https prefix when ClickAction.type is 4')

    @classmethod
    def check_light_settings(cls, color, light_on_duration, light_off_duration):
        cls.check_type(color, AndroidLightSettingsColor, "color must be an instance of AndroidLightSettingsColor")
        cls.check_string(hint="AndroidLightSettings.light_on_duration", value=light_on_duration)
        cls.check_string(hint="AndroidLightSettings.light_off_duration", value=light_off_duration)

    @classmethod
    def check_light_settings_color(cls, alpha, red, green, blue):
        cls.check_number("AndroidLightSettingsColor.alpha", alpha)
        cls.check_number("AndroidLightSettingsColor.red", red)
        cls.check_number("AndroidLightSettingsColor.green", green)
        cls.check_number("AndroidLightSettingsColor.blue", blue)

    @classmethod
    def check_webpush_config(cls, headers, data, notification, hms_options):
        # headers
        cls.check_type(headers, WebPushHeader, "headers must be an instance of WebPushHeader")
        cls.check_string(hint="WebPushConfig.headers", value=data)
        cls.check_type(notification, WebPushNotification, "notification must be an instance of WebPushNotification")
        cls.check_type(hms_options, WebPushHMSOptions, "hms_options must be an instance of WebPushHMSOptions")

    @classmethod
    def check_webpush_header(cls, ttl=None, urgency=None, topic=None):
        cls.check_string(hint="WebPushHeader.ttl", value=ttl)
        cls.check_string(hint="WebPushHeader.urgency", value=urgency)
        cls.check_string(hint="WebPushHeader.topic", value=topic)

    @classmethod
    def check_webpush_notification(cls, title=None, body=None, icon=None, actions=None, badge=None,
                                   data=None, dir=None, image=None, lang=None, renotify=None,
                                   require_interaction=None, silent=None, tag=None, timestamp=None, vibrate=None):
        cls.check_string(hint="WebPushNotification.title", value=title)
        cls.check_string(hint="WebPushNotification.body", value=body)
        cls.check_string(hint="WebPushNotification.icon", value=icon)
        cls.check_string(hint="WebPushNotification.data", value=data)
        cls.check_type_list("WebPushNotificationAction.actions", actions, WebPushNotificationAction)
        cls.check_string(hint="WebPushNotification.image", value=image)
        cls.check_string(hint="WebPushNotification.lang", value=lang)
        cls.check_string(hint="WebPushNotification.tag", value=tag)
        cls.check_string(hint="WebPushNotification.badge", value=badge)
        cls.assert_string_values("WebPushNotification.dir", dir, "auto", "ltr", "rtl")
        cls.check_number_list("WebPushNotification.vibrate", vibrate)
        cls.check_boolean("WebPushNotification.renotify", renotify)
        cls.check_boolean("WebPushNotification.require_interaction", require_interaction)
        cls.check_boolean("WebPushNotification.silent", silent)
        cls.check_number("WebPushNotification.timestamp", timestamp)

    @classmethod
    def check_webpush_notification_action(cls, action=None, title=None, icon=None):
        cls.check_string(hint="WebPushNotificationAction.action", value=action)
        cls.check_string(hint="WebPushNotificationAction.title", value=title)
        cls.check_string(hint="WebPushNotificationAction.icon", value=icon)

    @classmethod
    def check_webpush_hms_options(cls, link):
        cls.check_string(hint="WebPushHMSOptions.link", value=link)

    @classmethod
    def check_apns_config(cls, headers=None, payload=None, apns_hms_options=None):
        cls.check_string_dict("APNsConfig.headers", headers)
        cls.check_type(payload, APNsPayload, "payload must be an instance of APNsPayload")
        cls.check_type(apns_hms_options, APNsHMSOptions, "apns_hms_options must be an instance of APNsHMSOptions")

    @classmethod
    def check_apns_payload(cls, aps=None):
        cls.check_type(aps, APNsAps, "aps must be an instance of APNsAps")
        pass

    @classmethod
    def check_apns_payload_aps(cls, alert, badge, sound, content_available, category, thread_id, mutable_content,
                               custom_data):
        # alert: Dictionary or String
        if alert is not None:
            if not isinstance(alert, six.string_types):
                cls.check_type(alert, APNsAlert, "alert must be an instance of String or APNsAlert class")
        # badge: Number
        cls.check_number("APNsAps.badge", badge)
        # sound: String
        cls.check_string("APNsAps.sound", sound)
        # content_available: number
        cls.check_number("APNsAps.content_available", content_available)
        # category: String
        cls.check_string("APNsAps.category", category)
        # thread_id: String
        cls.check_string("APNsAps.thread_id", thread_id)
        # mutable_content
        cls.check_boolean("APNsAps.mutable_content", mutable_content)
        # custom_data
        if custom_data is not None:
            if not isinstance(custom_data, dict):
                raise ValueError('APNsAps.custom_data must be a dict.')

    @classmethod
    def check_apns_payload_aps_alert(cls, title, body, loc_key, loc_args, title_loc_key, title_loc_args, action_loc_key,
                                     launch_image, custom_data):
        # title: String
        cls.check_string("APNsAlert.title", title)
        # body: String
        cls.check_string("APNsAlert.body", body)
        # loc_key: String
        cls.check_string("APNsAlert.loc_key", loc_key)
        # loc_args: Array of strings
        cls.check_string_list("APNsAlert.loc_args", loc_args)
        # title_loc_key: String or null
        cls.check_string("APNsAlert.title_loc_key", title_loc_key)
        # title_loc_args: Array of strings or null
        cls.check_string_list("APNsAlert.title_loc_args", title_loc_args)
        # action_loc_key: String or null
        cls.check_string("APNsAlert.action_loc_key", action_loc_key)
        # launch_image: String
        cls.check_string("APNsAlert.launch_image", launch_image)
        # custom_data
        if custom_data is not None:
            if not isinstance(custom_data, dict):
                raise ValueError('APNsAlert.custom_data must be a dict.')

    @classmethod
    def check_apns_hms_options(cls, target_user_type):
        cls.assert_integer_values("APNsHMSOptions.target_user_type", target_user_type, 1, 2, 3)
