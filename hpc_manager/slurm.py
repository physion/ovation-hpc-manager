import logging
import paramiko
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
                        api=None,
                        head_node=None,
                        key_filename=None,
                        host_key_file=None,
                        ssh_username=None):
    """Handle pubsub message to submit a job.
    :param msg google.cloud.pubsub_v1.subscriber.message.Message
    :returns (job_response, token_info) : job_response as dict, token_info to pass to service.make_session
    """

    logging.info("Received message: {}".format(msg))

    if ((not 'activity_id' in msg) or
            (not 'organization' in msg) or
            (not 'image_name' in msg) or
            (not 'token' in msg)):
        raise MessageException("Missing required message attributes")

    activity_id = msg['activity_id']
    image_name = msg['image_name']
    org = msg['organization']
    token = msg['token']

    (updated_token_info, session) = service.make_session(token_info,
                                                         organization=org,
                                                         client_id=client_id,
                                                         client_secret=client_secret,
                                                         auth=auth_domain,
                                                         audience=audience,
                                                         api=api)

    logging.info("Connecting to head node")
    client = paramiko.SSHClient()
    client.connect(head_node,
                   key_filename=key_filename,
                   allow_agent=False,
                   look_for_keys=False,
                   host_key_file=host_key_file,
                   username=ssh_username)

    try:
        stdin, stdout, stderr = client.exec_command('~/core.sh {token} {activity_id} {image}'.format(token=token,
                                                                                                     activity_id=activity_id,
                                                                                             image=image_name))
        if stdout.channel.recv_exit_status() != 0:
            raise SlurmException(stderr.read())

        return stdout.read(), updated_token_info

    except paramiko.SSHException as ex:
        logging.exception(str(ex), exc_info=True)
        raise ex
    finally:
        client.close()

