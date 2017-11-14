import ovation.hpc.config as config
import ovation.hpc.pubsub as pubsub

from ovation.hpc.slurm import submit_research_job

def make_system():
    # PubSub client
    cb = pubsub.make_research_callback(submit_research_job,
                                       client_id=config.secret('OVATION_CLIENT_ID'),
                                       client_secret=config.secret('OVATION_CLIENT_SECRET'),
                                       auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
                                       audience=config.configuration('OVATION_AUDIENCE'),
                                       ovation_api=config.configuration('OVATION_API_URL'))

    pubsub.open_subscription(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                             config.configuration('PUBSUB_REQUESTS_TOPIC'),
                             subscription_name=config.configuration('PUBSUB_REQUEST_SUBSCRIPTION_NAME', None),
                             callback=cb)

    return None
