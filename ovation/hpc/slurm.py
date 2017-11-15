import logging


class SlurmException(Exception):
    pass


class MessageException(Exception):
    pass


def submit_research_job(msg):
    """Handle pubsub message to submit a job.
    :param msg google.cloud.pubsub_v1.subscriber.message.Message
    :returns (job_response, token_info) : job_response as dict, token_info to pass to service.make_session
    """

    logging.info("Received message: {}".format(msg))

    if ((not 'activity_id' in msg) or
            (not 'image_rev' in msg)):
        raise MessageException("Missing required message attributes")

    activity_id = msg['activity_id']
    image_rev = msg['image_rev']

    upload

    job_response = ''

    return job_response
