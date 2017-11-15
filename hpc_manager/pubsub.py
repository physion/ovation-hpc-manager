import copy
import json
import logging
import uuid

from google.cloud import pubsub


def make_research_callback(submit_job,
                           token_info=None,
                           client_id=None,
                           client_secret=None,
                           auth_domain=None,
                           audience=None,
                           ovation_api=None,
                           head_node='scc.alphacruncher.net',
                           key_filename='/var/secret/id_rsa',
                           host_key_file='/var/secret/known_hosts'):

    token_info = copy.deepcopy(token_info) if token_info else {}

    def callback(message):
        local_token_info = copy.deepcopy(token_info) if (token_info is not None and len(token_info) > 0) else None

        try:
            logging.info('Starting: {}'.format(message.message_id))
            msg = json.loads(message.data.decode('utf-8'))

            job, updated_token_info = submit_job(msg,
                                                 token_info=local_token_info,
                                                 client_id=client_id,
                                                 client_secret=client_secret,
                                                 auth_domain=auth_domain,
                                                 audience=audience,
                                                 api=ovation_api,
                                                 head_node=head_node,
                                                 key_filename=key_filename,
                                                 host_key_file=host_key_file)

            logging.info('Complete: {}'.format(message.message_id))
            message.ack()

            token_info.update(updated_token_info)

            return job

        except Exception as ex:
            logging.exception("Failed: {}".format(message.message_id))
            logging.exception("Error indexing", exc_info=True)
            message.nack()
            return None

    return callback


def open_subscription(project_id, topic, subscription_name=None, callback=None):
    subscriber = pubsub.SubscriberClient()
    topic_path = subscriber.topic_path(project_id, topic)

    if subscription_name is None:
        subscription_name = "indexer-{}".format(uuid.uuid4())

    subscription_path = subscriber.subscription_path(project_id, subscription_name)

    # Create subscription if needed
    try:
        subscriber.create_subscription(subscription_path, topic_path)
    except BaseException:
        logging.info("Subscription {} already exists".format(subscription_path))

    subscriber.subscribe(subscription_path, callback)

# def publish_messages(project, topic_name):
#     """Publishes multiple messages to a Pub/Sub topic."""
#     publisher = pubsub.PublisherClient()
#     topic_path = publisher.topic_path(project, topic_name)
#
#     for n in range(1, 10):
#         data = {"activity_id": n,
#                 "user_id": 8,
#                 "container_revision_id": 3}
#         # Data must be a bytestring
#         data = json.dumps(data).encode('utf-8')
#         publisher.publish(topic_path, data=data)
#
#     print('Published messages.')
