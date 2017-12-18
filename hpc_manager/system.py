import falcon


def make_system():
    application = falcon.API()
    application.add_route('/hpc_run', app.HpcHandler())

    # TODO should set up pubsub here

    return application
