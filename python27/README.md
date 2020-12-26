# HMS Pushkit Python Severdemo

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
| examples     |    Sample code packages. Each package can run independently.|
| push_admin   |    Package where APIs of the HUAWEI Push Kit server are encapsulated.|
	
## Installation

To install pushkit-python-sample, you should extract the compressed ZIP file, execute the following command in the unzipped directory:
```
python setup.py install
```

## Supported Environments
For pushkit-python-sample, We currently support Python 2.7/3.7 and JetBrains PyCharm are recommended.


## Configuration 
The following table describes parameters of the initialize_app method.

| Parameter      |    Description |
| -------------  |   ------------------------------------------------------------------------- |
| appid          |    App ID, which is obtained from app information. |
| appsecret      |    Secret access key of an app, which is obtained from app information. |
| token_server   |    URL for the Huawei OAuth 2.0 service to obtain a token, please refer to [Generating an App-Level Access Token](https://developer.huawei.com/consumer/en/doc/development/parts-Guides/generating_app_level_access_token). |
| push_open_url  |    URL for accessing HUAWEI Push Kit, please refer to [Sending Messages](https://developer.huawei.com/consumer/en/doc/development/HMS-References/push-sendapi).||


## Sample Code
Download Python sample code in Downloading Server Sample Code.


Python sample code uses the Messaging structure in the push_admin package as the entry. Each method in the Messaging 
structure calls an API of the HUAWEI Push Kit server.

The following table describes methods in the Messaging structure.

| Method              |     Description
| -----------------   |     --------------------------------------------------- |
| send_message        |     Sends a message to a device. |
| subscribe_topic     |     Subscribes to a topic. |
| unsubscribe_topic   |     Unsubscribes from a topic. |
| list_topics         |     Queries the list of topics subscribed by a device. |
| initialize_app      |     Initializes the configuration parameters. |


1) Send an Android data message.
Code location: examples/send_data_message.py

2) Send an Android notification message.
Code location: examples/send_notify_message.py

3) Send a message by topic.
Code location: examples/send_topic_message.py

4) Send a message by conditions.
Code location: examples/send_condition_message.py

5) Send a message to a Huawei quick app.
Code location: examples/send_instance_app_message.py

6) Send a message through the WebPush agent.
Code location: examples/send_webpush_message.py

7) Send a message through the APNs agent.
Code location: examples/send_apns_message.py

8) Send a test message.
Code location: examples/send_test_message.py

## Libraries
| Library             |     Site
| -----------------   |     --------------------------------------------------- |
| requests            |     https://requests.readthedocs.io/en/master/ |
| six                 |     https://six.readthedocs.io/   |

## Question or issues
If you want to evaluate more about HMS Core,
[r/HMSCore on Reddit](https://www.reddit.com/r/HuaweiDevelopers/) is for you to keep up with latest news about HMS Core, and to exchange insights with other developers.
>>>>>>> afe8071b1b807b52ae92e6f1fd2255e0911150a9:README.md

If you have questions about how to use HMS samples, try the following options:
- [Stack Overflow](https://stackoverflow.com/questions/tagged/huawei-mobile-services) is the best place for any programming questions. Be sure to tag your question with 
`huawei-mobile-services`.
- [Huawei Developer Forum](https://forums.developer.huawei.com/forumPortal/en/home?fid=0101187876626530001) HMS Core Module is great for general questions, or seeking recommendations and opinions.

If you run into a bug in our samples, please submit an [issue](https://github.com/HMS-Core/hms-push-serverdemo-python/issues) to the Repository. Even better you can submit a [Pull Request](https://github.com/HMS-Core/hms-push-serverdemo-python/pulls) with a fix.

## License
pushkit Python sample is licensed under the [Apache License, version 2.0](http://www.apache.org/licenses/LICENSE-2.0).
