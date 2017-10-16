from google.cloud import pubsub_v1
import time
import json

def publish_messages(project, topic_name):
    """Publishes multiple messages to a Pub/Sub topic."""
    publisher = pubsub_v1.PublisherClient()
    topic_path = publisher.topic_path(project, topic_name)

    for n in range(1, 10):
        data = {"activity_id": n,
                "user_id": 8,
                "container_revision_id": 3}
        # Data must be a bytestring
        data = json.dumps(data)
        publisher.publish(topic_path, data=data)

    print('Published messages.')


#publish_messages(,)