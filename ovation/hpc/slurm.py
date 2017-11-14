import logging


def submit_research_job(msg):
    """Handle pubsub message to submit a job.
    :param msg google.cloud.pubsub_v1.subscriber.message.Message
    :returns (job_response, token_info) : job_response as dict, token_info to pass to service.make_session
    """

    logging.info("Received message: {}".format(msg))
    if ((not 'organization' in msg) or
            (not 'id' in msg) or
            (not 'type' in msg)):
        # TODO error
        return

    org = msg['organization']
    doc_id = msg['id']
    doc_type = msg['type']

    job_response = ''

    return job_response
