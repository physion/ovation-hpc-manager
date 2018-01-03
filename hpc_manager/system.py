import falcon
import hpc_manager.app as app
import hpc_manager.middleware as middleware


def make_system():
    application = falcon.API(middleware=[middleware.RequestLoggerMiddleware()])
    #application = falcon.API()
    application.add_route('/hpc_run', app.HpcRunResource())
    application.add_route('/', app.StatusResource())
    application.add_route('/status', app.StatusResource())

    # cb = pubsub.make_research_callback(submit_research_job,
    #                                    client_id=config.secret('OVATION_CLIENT_ID'),
    #                                    client_secret=config.secret('OVATION_CLIENT_SECRET'),
    #                                    auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
    #                                    audience=config.configuration('OVATION_AUDIENCE'),
    #                                    ovation_api=config.configuration('OVATION_API_URL'),
    #                                    head_node=config.configuration('CLUSTER_HEAD_NODE'),
    #                                    key_filename=config.configuration('SSH_KEY_FILE'),
    #                                    host_key_file=config.configuration('KNOWN_HOSTS_FILE'),
    #                                    ssh_username=config.configuration('SSH_USERNAME'))
    #
    # threading.Thread(target=pubsub.open_subscription,
    #                  name='pubsub-subscription',
    #                  args=(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
    #                        config.configuration('PUBSUB_REQUESTS_TOPIC')),
    #                  kwargs={
    #                      'subscription_name': config.configuration('PUBSUB_REQUEST_SUBSCRIPTION_NAME', None),
    #                      'callback': cb}).start()

    return application
