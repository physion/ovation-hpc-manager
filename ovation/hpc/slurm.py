import logging
import ovation.service as service


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
    if ((not 'organization' in msg) or
            (not 'id' in msg) or
            (not 'type' in msg)):
        # TODO error
        return

    org = msg['organization']
    doc_id = msg['id']
    doc_type = msg['type']

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
