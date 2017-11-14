import base64
import json

import ovation.hpc.pubsub as pubsub

from unittest.mock import Mock, sentinel, patch


def test_submit_job_callback_submits_job():
    submit_job = Mock()
    submit_job.return_value = sentinel.submit_response

    message = Mock()
    msg = {}
    message.data = json.dumps(msg).encode('utf-8')

    # Act
    cb = pubsub.make_research_callback(submit_job)

    result = cb(message)

    # Assert
    submit_job.assert_called_once_with(msg)

    assert result == sentinel.submit_response


@patch("google.cloud.pubsub.SubscriberClient")
def test_open_subscription_creates_subscription(SubscriberClient):
    subscriber = Mock()
    SubscriberClient.return_value = subscriber

    subscriber.subscription_path.return_value = sentinel.subscription_path
    subscriber.topic_path.return_value = sentinel.topic_path

    pubsub.open_subscription(sentinel.project_id,
                             sentinel.topic,
                             subscription_name=sentinel.subscription_name,
                             callback=sentinel.callback)

    subscriber.topic_path.assert_called_with(sentinel.project_id, sentinel.topic)

    subscriber.subscription_path.assert_called_with(sentinel.project_id,
                                                    sentinel.subscription_name)

    subscriber.create_subscription.assert_called_with(sentinel.subscription_path,
                                                      sentinel.topic_path)


@patch("google.cloud.pubsub.SubscriberClient")
def test_open_subscription_subscribes(SubscriberClient):
    subscriber = Mock()
    SubscriberClient.return_value = subscriber

    subscriber.subscription_path.return_value = sentinel.subscription_path
    subscriber.topic_path.return_value = sentinel.topic_path

    pubsub.open_subscription(sentinel.project_id,
                             sentinel.topic,
                             subscription_name=sentinel.subscription_name,
                             callback=sentinel.callback)

    subscriber.subscribe.assert_called_with(sentinel.subscription_path, sentinel.callback)
