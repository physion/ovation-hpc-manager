import hpc_manager.config as config
import hpc_manager.pubsub as pubsub
import falcon
import threading

from hpc_manager.slurm import submit_research_job


def make_system():
    # PubSub client
    cb = pubsub.make_research_callback(submit_research_job,
                                       client_id=config.secret('OVATION_CLIENT_ID'),
                                       client_secret=config.secret('OVATION_CLIENT_SECRET'),
                                       auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
                                       audience=config.configuration('OVATION_AUDIENCE'),
                                       ovation_api=config.configuration('OVATION_API_URL'),
                                       head_node=config.configuration('CLUSTER_HEAD_NODE'),
                                       key_filename=config.configuration('SSH_KEY_FILE'),
                                       host_key_file=config.configuration('KNOWN_HOSTS_FILE'),
                                       ssh_username=config.configuration('SSH_USERNAME'))

    pubsub.open_subscription(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                             config.configuration('PUBSUB_REQUESTS_TOPIC'),
                             subscription_name=config.configuration('PUBSUB_REQUEST_SUBSCRIPTION_NAME', None),
                             callback=cb)

    return None


def make_api():
    api = falcon.API()
    api.add_route('/hpc_run', falcon.HTTP_200)
    # PubSub client
    cb = pubsub.make_research_callback(submit_research_job,
                                       client_id=config.secret('OVATION_CLIENT_ID'),
                                       client_secret=config.secret('OVATION_CLIENT_SECRET'),
                                       auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
                                       audience=config.configuration('OVATION_AUDIENCE'),
                                       ovation_api=config.configuration('OVATION_API_URL'),
                                       head_node=config.configuration('CLUSTER_HEAD_NODE'),
                                       key_filename=config.configuration('SSH_KEY_FILE'),
                                       host_key_file=config.configuration('KNOWN_HOSTS_FILE'),
                                       ssh_username=config.configuration('SSH_USERNAME'))

    threading.Thread(target=pubsub.open_subscription,
                     name='pubsub-subscription',
                     args=(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                           config.configuration('PUBSUB_REQUESTS_TOPIC'),
                           config.configuration('PUBSUB_REQUEST_SUBSCRIPTION_NAME', None),
                           cb),
                     kwargs={
                         'subscription_name': config.configuration('PUBSUB_REQUEST_SUBSCRIPTION_NAME', None),
                         'callback': cb}).start()

    return api

