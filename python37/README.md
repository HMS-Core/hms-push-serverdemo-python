## HMS PushKit Python Severdemo
English | [中文](README_ZH.md)

## Table of Contents

 * [Introduction](#introduction)
 * [Installation](#installation)
 * [Configuration ](#configuration )
 * [Supported Environments](#supported-environments)
 * [Sample Code](#sample-code)
 * [Libraries](#Libraries)
 * [License](#license)
 
 
## Introduction

Python sample code encapsulates APIs of the HUAWEI Push Kit server. It provides many sample programs about quick access to HUAWEI Push Kit for your reference or usage.

The following table describes packages of Python sample code.

| Package      |    Description |
| ----------   |    ------------|
| [test](test)     |    Sample code packages. Each package can run independently.|
| [src/push_admin](src/push_admin)   |    Package where APIs of the HUAWEI Push Kit server are encapsulated.|
	
## Installation

To install pushkit-python-sample, you should extract the compressed ZIP file, execute the following command in the unzipped directory:
```
python setup.py install
```

## Supported Environments
For pushkit-python-sample, We currently support Python 3.7 and JetBrains PyCharm are recommended.


## Configuration 
The following table describes parameters of the initialize_app method.

| Parameter      |    Description |
| -------------  |   ------------------------------------------------------------------------- |
| app_id          |    App ID, which is obtained from app information. |
| app_secret      |    Secret access key of an app, which is obtained from app information. |
| app_package_name      |    Appplication package name. |
| token_server   |    URL for the Huawei OAuth 2.0 service to obtain a token, please refer to [Generating an App-Level Access Token](https://developer.huawei.com/consumer/en/doc/development/HMSCore-Guides/oauth2-0000001212610981). |
| push_open_url  |    URL for accessing HUAWEI Push Kit, please refer to [Sending Messages](https://developer.huawei.com/consumer/en/doc/development/HMSCore-Guides/android-server-dev-0000001050040110?ha_source=hms1).||


## Sample Code

Python sample code uses the Messaging structure in the push_admin package as the entry. Each method in the Messaging 
structure calls an API of the HUAWEI Push Kit server.

The following table describes methods in the Messaging structure.

| Method              |     Description
| -----------------   |     --------------------------------------------------- |
| send_message        |     Sends a message to a device. |
| subscribe_topic     |     Subscribes to a topic. |
| unsubscribe_topic   |     Unsubscribes from a topic. |
| list_topics         |     Queries the list of topics subscribed by a device. |

1) Send an Android data message.
Code location: [test/send_data_message.py](test/send_data_message.py)

2) Send an Android notification message.
Code location: [test/send_notify_message.py](test/send_notify_message.py)

3) Send a message by topic.
Code location: [test/send_topic_message.py](test/send_topic_message.py)

4) Send a message by conditions.
Code location: [test/send_condition_message.py](test/send_condition_message.py)

5) Send a message to a Huawei quick app.
Code location: [test/send_instance_app_message.py](test/send_instance_app_message.py)

6) Send a message through the WebPush agent.
Code location: [test/send_webpush_message.py](test/send_webpush_message.py)

7) Send a message through the APNs agent.
Code location: [test/send_apns_message.py](test/send_apns_message.py)

8) Send a test message.
Code location: [test/send_test_message.py](test/send_test_message.py)

## Libraries
| Library             |     Site
| -----------------   |     --------------------------------------------------- |
| requests            |     https://requests.readthedocs.io/en/master/ |
| six                 |     https://six.readthedocs.io/   |
## License

pushkit Python sample is licensed under the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
