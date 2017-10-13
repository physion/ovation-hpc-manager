from google.cloud import pubsub_v1
import time


def create_subscription(project, topic_name, subscription_name):
    subscriber = pubsub_v1.SubscriberClient()
    topic = 'projects/{project_id}/topics/{topic}'.format( project_id = project, topic = topic_name)
    subscription_name = 'projects/{project_id}/subscriptions/{sub}'.format(project_id = project,
                                                                           sub = subscription_name)
    subscriber.create_subscription(subscription_name, topic)


def receive_messages(project, subscription_name):
    """Receives messages from a pull subscription."""
    subscriber = pubsub_v1.SubscriberClient()
    subscription_path = subscriber.subscription_path(
        project, subscription_name)

    def callback(message):
        print('Received message: {}'.format(message))
        message.ack()

    subscriber.subscribe(subscription_path, callback=callback)

    # The subscriber is non-blocking, so we must keep the main thread from
    # exiting to allow it to process messages in the background.
    print('Listening for messages on {}'.format(subscription_path))
    while True:
        time.sleep(60)


#create_subscription(,, "subscription_test")
#receive_messages(, "subscription_test")