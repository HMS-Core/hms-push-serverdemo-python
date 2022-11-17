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

import json
from src.push_admin import _messages
import six


class MessageSerializer(json.JSONEncoder):
    """
    Use https://docs.python.org/3/library/json.html to do serialization

    The serializer should serialize the following messages:
    _messages.Message
    _messages.Notification
    _messages.ApnsConfig
    _messages.WebPushConfig
    _messages.WebPushNotification
    _messages.WebPushNotificationAction
    _messages.WebPushHMSOptions
    _messages.AndroidConfig
    _messages.AndroidNotification
    _messages.AndroidClickAction
    _messages.BadgeNotification
    """
    def default(self, message):
        """
        :param message: The push message
        :return: formatted push messages
        """
        result = {
            'data': message.data,
            'notification': MessageSerializer.encode_notification(message.notification),
            'android': MessageSerializer.encode_android_config(message.android),
            'apns': MessageSerializer.encode_apns_config(message.apns),
            'webpush': MessageSerializer.encode_webpush_config(message.web_push),
            'token': message.token,
            'topic': message.topic,
            'condition': message.condition
        }
        result = MessageSerializer.remove_null_values(result)
        return result

    @classmethod
    def remove_null_values(cls, dict_value):
        return {k: v for k, v in dict_value.items() if v not in [None, [], {}]}

    @classmethod
    def encode_notification(cls, notification):
        """
            An example:
           {
              "title":"Big News",
              "body":"This is a Big News!",
              "image":"https://res.vmallres.com/pimages//common/config/logo/SXppnESYv4K11DBxDFc2.png"
            }
        :param notification:
        :return:
        """
        if notification is None:
            return None

        if not isinstance(notification, _messages.Notification):
            raise ValueError('Message.notification must be an instance of Notification class.')

        result = {
            'title': notification.title,
            'body': notification.body,
            'image': notification.image
        }
        return cls.remove_null_values(result)

    @classmethod
    def encode_android_config(cls, android_config):
        """
        An example:
        {
          "android":{
            "collapse_key":-1,
            "urgency":"HIGH",
            "ttl":"1448s",
            "bi_tag":"Trump",
            "fast_app_target":1,
            "notification": {}
        }
        :param android_config:
        :return:
        """
        if android_config is None:
            return None

        if not isinstance(android_config, _messages.AndroidConfig):
            raise ValueError('Message.android must be an instance of AndroidConfig class.')

        result = {
            'collapse_key': android_config.collapse_key,
            'urgency': android_config.urgency,
            'ttl': android_config.ttl,
            'bi_tag': android_config.bi_tag,
            'fast_app_target': android_config.fast_app_target,
            'data': android_config.data,
            'notification': MessageSerializer.encode_android_notification(android_config.notification)
        }
        return cls.remove_null_values(result)

    @classmethod
    def encode_android_notification(cls, notification):
        """
           "notification":{
                "title":"test title",
                "body":"test body",
                "icon":"https://res.vmallres.com/pimages//common/config/logo/SXppnESYv4K11DBxDFc2.png",
                "color":"#AACCDD",
                "sound":"http://att.chinauui.com/day_120606/20120606_7fcf2235b44f1eab0b4dadtAkAGMTBHK.mp3",
                "default_sound":true,
                "tag":"tagBoom",
                "importance":"PRIORITY_HIGH",
                "click_action":{
                    "type":2,
                    "url":"https://www.huawei.com"
                },
                "body_loc_key":"M.String.body",
                "body_loc_args":[
                    "Boy",
                    "Dog"
                ],
                "title_loc_key":"M.String.title",
                "title_loc_args":[
                    "Girl",
                    "Cat"
                ],
                "channel_id":"RingRing",
                "notify_summary":"Some Summary",
                "style":2,
                "big_title":"Big Title",
                "big_body":"Big Body",
                "notify_id":123,
                "group":"spaceGroup",
                "badge":{
                    "add_num":99,
                    "set_num":99,
                    "class":"Classic"
                },
                "ticker":"i am a ticker",
                "auto_cancel":false,
                "when":"2019-11-05",
                "use_default_vibrate":true,
                "use_default_light":false,
                "visibility":"PUBLIC",
                "vibrate_config":["1.5","2","3"],
                "light_settings":{
                    "color":{
                        "alpha":0,
                        "red":0,
                        "green":1,
                        "blue":1
                    },
                    "light_on_duration":"3.5",
                    "light_off_duration":"5S"
                },
                "foreground_show":true
              }
        :param notification:
        :return:
        """
        if notification is None:
            return None

        if not isinstance(notification, _messages.AndroidNotification):
            raise ValueError('Message.AndroidConfig.notification must be an instance of AndroidNotification class.')

        result = {
            "title": notification.title,
            "body": notification.body,
            "icon": notification.icon,
            "color": notification.color,
            "sound": notification.sound,
            "default_sound": notification.default_sound,
            "tag": notification.tag,
            "importance": notification.importance,
            "multi_lang_key": notification.multi_lang_key,
            "click_action": MessageSerializer.encode_android_click_action(notification.click_action),
            "body_loc_key": notification.body_loc_key,
            "body_loc_args": notification.body_loc_args,
            "title_loc_key": notification.title_loc_key,
            "title_loc_args": notification.title_loc_args,
            "channel_id": notification.channel_id,
            "notify_summary": notification.notify_summary,
            "image": notification.image,
            "style": notification.style,
            "big_title": notification.big_title,
            "big_body": notification.big_body,
            "notify_id": notification.notify_id,
            "group": notification.group,
            "badge": MessageSerializer.encode_android_badge(notification.badge),
            "ticker": notification.ticker,
            "auto_cancel": notification.auto_cancel,
            "when": notification.when,
            "use_default_vibrate": notification.use_default_vibrate,
            "use_default_light": notification.use_default_light,
            "visibility": notification.visibility,
            "vibrate_config": notification.vibrate_config,
            "light_settings": MessageSerializer.encode_android_light_settings(notification.light_settings),
            "foreground_show": notification.foreground_show
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_android_click_action(cls, click_action):
        """
            "click_action":{
                    "type":2,
                    "url":"https://www.huawei.com"
             }

             "click_action":{
                    "type":1,
                    "intent":"https://www.huawei.com",
                    "action":""
             }

        :param click_action: _messages.AndroidClickAction
        :return:
        """
        if click_action is None:
            return None

        if not isinstance(click_action, _messages.AndroidClickAction):
            raise ValueError('Message.AndroidConfig.AndroidNotification.click_action must be an instance\
                             of AndroidClickAction class.')

        result = {
            "type": click_action.action_type,
            "intent": click_action.intent,
            "url": click_action.url,
            "action": click_action.action
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_android_badge(cls, badge):
        """
        refer to: _messages.AndroidBadgeNotification

        "badge":{
                    "add_num":99,
                    "set_num":99,
                    "class":"Classic"
                }

        :param badge:
        :return:
        """
        if badge is None:
            return None

        if not isinstance(badge, _messages.AndroidBadgeNotification):
            raise ValueError('Message.AndroidConfig.AndroidNotification.badge must be an instance\
                             of AndroidBadgeNotification class.')

        result = {
            "add_num": badge.add_num,
            "set_num": badge.set_num,
            "class": badge.clazz
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_android_light_settings(cls, android_light_settings):
        """
        refer to: _messages.AndroidLightSettings

        "light_settings":{
                "color":{
                        "alpha":0,
                        "red":0,
                        "green":1,
                        "blue":1
                },
                "light_on_duration":"3.5",
                "light_off_duration":"5S"
         }

        :param android_light_settings:  _messages.AndroidLightSettings
        :return:
        """
        if android_light_settings is None:
            return None

        if not isinstance(android_light_settings, _messages.AndroidLightSettings):
            raise ValueError('Message.AndroidConfig.AndroidNotification.android_light_settings must be an instance\
                             of AndroidLightSettings class.')

        result = {
            "color": MessageSerializer.encode_android_light_settings_color(android_light_settings.color),
            "light_on_duration": android_light_settings.light_on_duration,
            "light_off_duration": android_light_settings.light_off_duration
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_android_light_settings_color(cls, color):
        """
        "color":{
                        "alpha":0,
                        "red":0,
                        "green":1,
                        "blue":1
        }

        :param color: _messages.AndroidLightSettingsColor
        :return:
        """
        if color is None:
            return None

        if not isinstance(color, _messages.AndroidLightSettingsColor):
            raise ValueError('Message.AndroidConfig.AndroidNotification.android_light_settings.color must be an instance\
                             of AndroidLightSettingsColor class.')
        result = {
            "alpha": color.alpha,
            "red": color.red,
            "green": color.green,
            "blue": color.blue
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_webpush_config(cls, webpush_config):
        """
        "webpush":{
            "headers":{
                ...
            },
            "notification":{
                ...
            },
            "hms_options":{
                ...
            }
         }
        :param webpush_config: refer to _messages.WebPushConfig
        :return:
        """
        if webpush_config is None:
            return None

        if not isinstance(webpush_config, _messages.WebPushConfig):
            raise ValueError('Message.webpush must be an instance of WebPushConfig class.')

        result = {
            "headers": MessageSerializer.encode_webpush_config_headers(webpush_config.headers),
            "notification": MessageSerializer.encode_webpush_config_notification(webpush_config.notification),
            "hms_options": MessageSerializer.encode_webpush_config_hms_options(webpush_config.hms_options),
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_webpush_config_headers(cls, webpush_headers):
        """
        "headers":{
                "ttl":"990",
                "urgency":"very-low",
                "topic":"12313ceshi"
            }

        :param webpush_headers: _messages.WebPushHeader
        :return:
        """
        if webpush_headers is None:
            return None

        if not isinstance(webpush_headers, _messages.WebPushHeader):
            raise ValueError('Message.webpush.headers must be an instance of WebPushHeader class.')

        result = {
            "ttl": webpush_headers.ttl,
            "urgency": webpush_headers.urgency,
            "topic": webpush_headers.topic,
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_webpush_config_notification(cls, webpush_notification):
        """
        "notification":{
                "title":"notication string",
                "body":"web push body",
                "actions":[
                    {
                        "action":"",
                        "icon":"https://res.vmallres.com/pimages//common/config/logo/SXppnESYv4K11DBxDFc2.png",
                        "title":"string"
                    }
                ],
                "badge":"string",
                "dir":"auto",
                "icon":"https://res.vmallres.com/pimages//common/config/logo/SXppnESYv4K11DBxDFc2.png",
                "image":"string",
                "lang":"string",
                "renotify":true,
                "requireInteraction":true,
                "silent":true,
                "tag":"string",
                "timestamp":1545201266,
                "vibrate":[1,2,3]
            }

        :param webpush_notification: refer to _messages.WebPushNotification
        :return:
        """
        if webpush_notification is None:
            return None

        if not isinstance(webpush_notification, _messages.WebPushNotification):
            raise ValueError('Message.webpush.notification must be an instance of WebPushNotification class.')

        result = {
            "title": webpush_notification.title,
            "body": webpush_notification.body,
            "actions": [MessageSerializer.encode_webpush_notification_action(_)
                        for _ in webpush_notification.actions],
            "badge": webpush_notification.badge,
            "dir": webpush_notification.dir,
            "icon": webpush_notification.icon,
            "image": webpush_notification.image,
            "lang": webpush_notification.lang,
            "renotify": webpush_notification.renotify,
            "require_interaction": webpush_notification.require_interaction,
            "silent": webpush_notification.silent,
            "tag": webpush_notification.tag,
            "timestamp": webpush_notification.timestamp,
            "vibrate": webpush_notification.vibrate
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_webpush_notification_action(cls, webpush_notification_action):
        """
        "actions":[
                    {
                        "action":"",
                        "icon":"https://res.vmallres.com/pimages//common/config/logo/SXppnESYv4K11DBxDFc2.png",
                        "title":"string"
                    }
                ],
        :param webpush_notification_action: refer to _messages.WebPushNotificationAction
        :return:
        """
        if webpush_notification_action is None:
            return None

        if not isinstance(webpush_notification_action, _messages.WebPushNotificationAction):
            raise ValueError('Message.webpush.notification.action must be an instance of \
                            WebPushNotificationAction class.')

        result = {
            "action": webpush_notification_action.action,
            "icon": webpush_notification_action.icon,
            "title": webpush_notification_action.title
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_webpush_config_hms_options(cls, webpush_hms_options):
        """
        "hms_options":{
                "link":"https://www.huawei.com/"
         }

        :param webpush_hms_options: refer to _messages.WebPushHMSOptions
        :return:
        """
        if webpush_hms_options is None:
            return None

        if not isinstance(webpush_hms_options, _messages.WebPushHMSOptions):
            raise ValueError('Message.webpush.hmsoptions must be an instance of \
                            WebPushHMSOptions class.')

        result = {
            "link": webpush_hms_options.link
        }
        result = cls.remove_null_values(result)
        return result

    @classmethod
    def encode_apns_config(cls, apns_config):
        """
        Encode APNs config into JSON
        :param apns_config:
        :return:
        """
        if apns_config is None:
            return None
        if not isinstance(apns_config, _messages.APNsConfig):
            raise ValueError('Message.apns_config must be an instance of _messages.APNsConfig class.')

        result = {
            'headers': apns_config.headers,
            'payload': cls.encode_apns_payload(apns_config.payload),
            'hms_options': cls.encode_apns_hms_options(apns_config.apns_hms_options)
        }
        return cls.remove_null_values(result)

    @classmethod
    def encode_apns_payload(cls, apns_payload):
        """Encodes an ``APNSPayload`` instance into JSON."""
        if apns_payload is None:
            return None
        if not isinstance(apns_payload, _messages.APNsPayload):
            raise ValueError('APNSConfig.payload must be an instance of _messages.APNsPayload class.')
        result = {
            'aps': cls.encode_apns_payload_aps(apns_payload.aps)
        }
        for key, value in apns_payload.custom_data.items():
            result[key] = value
        return cls.remove_null_values(result)

    @classmethod
    def encode_apns_payload_aps(cls, apns_payload_aps):
        """Encodes an ``Aps`` instance into JSON."""
        if not isinstance(apns_payload_aps, _messages.APNsAps):
            raise ValueError('APNSPayload.aps must be an instance of _messages.APNsAps class.')

        result = {
            'alert': cls.encode_apns_payload_alert(apns_payload_aps.alert),
            'badge': apns_payload_aps.badge,
            'sound': apns_payload_aps.sound,
            'category': apns_payload_aps.category,
            'thread-id': apns_payload_aps.thread_id
        }

        if apns_payload_aps.content_available is True:
            result['content-available'] = 1
        if apns_payload_aps.mutable_content is True:
            result['mutable-content'] = 1
        if apns_payload_aps.custom_data is not None:
            if not isinstance(apns_payload_aps.custom_data, dict):
                raise ValueError('Aps.custom_data must be a dict.')
            for key, val in apns_payload_aps.custom_data.items():
                if key in result:
                    raise ValueError('Multiple specifications for {0} in Aps.'.format(key))
                result[key] = val
        return cls.remove_null_values(result)

    @classmethod
    def encode_apns_payload_alert(cls, apns_payload_alert):
        """Encodes an ``ApsAlert`` instance into JSON."""
        if apns_payload_alert is None:
            return None
        if isinstance(apns_payload_alert, six.string_types):
            return apns_payload_alert
        if not isinstance(apns_payload_alert, _messages.APNsAlert):
            raise ValueError('Aps.alert must be a string or an instance of _messages.APNsAlert class.')
        result = {
            'title': apns_payload_alert.title,
            'body': apns_payload_alert.body,
            'title-loc-key': apns_payload_alert.title_loc_key,
            'title-loc-args': apns_payload_alert.title_loc_args,
            'loc-key': apns_payload_alert.loc_key,
            'loc-args': apns_payload_alert.loc_args,
            'action-loc-key': apns_payload_alert.action_loc_key,
            'launch-image': apns_payload_alert.launch_image
        }
        if result.get('loc-args') and not result.get('loc-key'):
            raise ValueError(
                'ApsAlert.loc_key is required when specifying loc_args.')
        if result.get('title-loc-args') and not result.get('title-loc-key'):
            raise ValueError(
                'ApsAlert.title_loc_key is required when specifying title_loc_args.')
        if apns_payload_alert.custom_data is not None:
            if not isinstance(apns_payload_alert.custom_data, dict):
                raise ValueError('ApsAlert.custom_data must be a dict.')
            for key, val in apns_payload_alert.custom_data.items():
                result[key] = val
        return cls.remove_null_values(result)

    @classmethod
    def encode_apns_hms_options(cls, apns_hms_options):
        """
        :param apns_hms_options:
        """
        if apns_hms_options is None:
            return None
        if not isinstance(apns_hms_options, _messages.APNsHMSOptions):
            raise ValueError('Aps.alert must be a string or an instance of _messages.APNsHMSOptions class.')

        result = {
            'target_user_type': apns_hms_options.target_user_type,
        }
        return cls.remove_null_values(result)
