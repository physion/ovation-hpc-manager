import json

import hpc_manager.pubsub as pubsub

from unittest.mock import Mock, sentinel, patch


def test_submit_job_callback_submits_job():
    submit_job = Mock()
    updated_token_info = {'key': 'new-value'}
    submit_job.return_value = sentinel.submit_response, updated_token_info

    message = Mock()
    msg = {}
    message.data = json.dumps(msg).encode('utf-8')

    # Act
    cb = pubsub.make_research_callback(submit_job,
                                       client_id=sentinel.client_id,
                                       client_secret=sentinel.client_secret,
                                       auth_domain=sentinel.auth_domain,
                                       audience=sentinel.audience,
                                       ovation_api=sentinel.ovation_api,
                                       head_node=sentinel.head_node,
                                       key_filename=sentinel.key_filename,
                                       host_key_file=sentinel.host_key_file,
                                       ssh_username=sentinel.username)

    result = cb(message)

    # Assert
    submit_job.assert_called_once_with(msg,
                                       token_info=None,
                                       client_id=sentinel.client_id,
                                       client_secret=sentinel.client_secret,
                                       auth_domain=sentinel.auth_domain,
                                       audience=sentinel.audience,
                                       api=sentinel.ovation_api,
                                       head_node=sentinel.head_node,
                                       key_filename=sentinel.key_filename,
                                       host_key_file=sentinel.host_key_file,
                                       ssh_username=sentinel.username)

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
                             callback=sentinel.callback,
                             restart_on_failure=False)

    subscriber.topic_path.assert_called_with(sentinel.project_id, sentinel.topic)

    subscriber.subscription_path.assert_called_with(sentinel.project_id,
                                                    sentinel.subscription_name)

    subscriber.create_subscription.assert_called_with(sentinel.subscription_path,
                                                      sentinel.topic_path)


@patch("google.cloud.pubsub.SubscriberClient")
def test_open_subscription_subscribes(SubscriberClient):
    subscriber = Mock()
    SubscriberClient.return_value = subscriber
    subscription = Mock()

    subscriber.subscription_path.return_value = sentinel.subscription_path
    subscriber.topic_path.return_value = sentinel.topic_path
    subscriber.subscribe.return_value = subscription

    pubsub.open_subscription(sentinel.project_id,
                             sentinel.topic,
                             subscription_name=sentinel.subscription_name,
                             callback=sentinel.callback,
                             restart_on_failure=False)

    subscriber.subscribe.assert_called_with(sentinel.subscription_path)
    subscription.open.assert_called_with(sentinel.callback)
