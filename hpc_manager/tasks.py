import hpc_manager.config as config


from hpc_manager.slurm import submit_research_job


def send_message(message):
    job, updated_token_info = submit_research_job(message,
                                                  client_id=config.secret('OVATION_CLIENT_ID'),
                                                  client_secret=config.secret('OVATION_CLIENT_SECRET'),
                                                  auth_domain=config.configuration('OVATION_AUTH_DOMAIN'),
                                                  audience=config.configuration('OVATION_AUDIENCE'),
                                                  api=config.configuration('OVATION_API_URL'),
                                                  head_node=config.configuration('CLUSTER_HEAD_NODE'),
                                                  key_filename=config.configuration('SSH_KEY_FILE'),
                                                  host_key_file=config.configuration('KNOWN_HOSTS_FILE'),
                                                  ssh_username=config.configuration('SSH_USERNAME'),
                                                  ovation_cli_args=config.configuration('OVATION_CLI_ARGS'))

