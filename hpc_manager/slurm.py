import logging
import ovation.service as service


class SlurmException(Exception):
    pass


class MessageException(Exception):
    pass


def submit_research_job(msg,
                        token_info=None,  # Will be created from client_id/client_secret if None
                        client_id=None,
                        client_secret=None,
                        auth_domain=None,
                        audience=None,
                        api=None):
    """Handle pubsub message to submit a job.
    :param msg google.cloud.pubsub_v1.subscriber.message.Message
    :returns (job_response, token_info) : job_response as dict, token_info to pass to service.make_session
    """

    logging.info("Received message: {}".format(msg))

    if ((not 'activity_id' in msg) or
            (not 'organization' in msg) or
            (not 'image_rev' in msg)):
        raise MessageException("Missing required message attributes")

    activity_id = msg['activity_id']
    image_rev = msg['image_rev']
    org = msg['organization']

    (updated_token_info, session) = service.make_session(token_info,
                                                         organization=org,
                                                         client_id=client_id,
                                                         client_secret=client_secret,
                                                         auth=auth_domain,
                                                         audience=audience,
                                                         api=api)
    token_info = updated_token_info

    job_response = ''

    return job_response, token_info
