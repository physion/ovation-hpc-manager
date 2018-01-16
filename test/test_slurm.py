import paramiko

import hpc_manager
import hpc_manager.slurm as slurm

import ovation.session as session
from unittest.mock import Mock, sentinel, patch


def test_submit_research_job_throws_message_exception_for_missing_attributes():
    try:
        slurm.submit_research_job({})
        assert False, "Should throw exception"
    except slurm.MessageException as ex:
        assert str(ex) == "Missing required message attributes"


@patch('paramiko.SSHClient')
@patch('ovation.service.make_session')
def test_submit_research_job_should_connect_to_head_node(make_session, ssh_client):
    s = Mock(spec=session.Session)
    make_session.return_value = (s, sentinel.token_info)

    client = Mock()
    ssh_client.return_value = client
    stdout = Mock()
    stderr = Mock()
    stdout.channel.recv_exit_status.return_value = 0
    client.exec_command.return_value = sentinel.stdin, stdout, stderr

    msg = {'activity_id': sentinel.activity_id,
           'organization': sentinel.org,
           'image_name': sentinel.image_name,
           'token': sentinel.token}

    slurm.submit_research_job(msg,
                              head_node=sentinel.head_node,
                              key_filename=sentinel.key_filename,
                              host_key_file=sentinel.host_key_file,
                              ssh_username=sentinel.username,
                              ovation_cli_args=sentinel.ovation_cli_args)

    # Assert
    client.load_host_keys.assert_called_with(sentinel.host_key_file)
    client.connect.assert_called_with(sentinel.head_node,
                                      key_filename=sentinel.key_filename,
                                      allow_agent=False,
                                      look_for_keys=False,
                                      username=sentinel.username,
                                      ovation_cli_args=sentinel.ovation_cli_args)


@patch('paramiko.SSHClient')
@patch('ovation.service.make_session')
def test_submit_research_job_should_submit_job(make_session, ssh_client):
    # s = Mock(spec=session.Session)
    # make_session.return_value = (sentinel.token_info, s)

    client = Mock()
    ssh_client.return_value = client

    stdout = Mock()
    stderr = Mock()
    stdout.channel.recv_exit_status.return_value = 0
    stdout.read.return_value = sentinel.job_output
    client.exec_command.return_value = sentinel.stdin, stdout, stderr

    msg = {'activity_id': sentinel.activity_id,
           'organization': sentinel.org,
           'image_name': sentinel.image_name,
           'token': sentinel.token}

    result = slurm.submit_research_job(msg,
                                       head_node=sentinel.head_node,
                                       key_filename=sentinel.key_filename)

    assert result == (sentinel.job_output, {})

    # Assert
    client.exec_command.assert_called_with(
        '~/bin/{ver}/ovation_core.sh {token} {activity} {image} {ovation_cli_args}'.format(ver=hpc_manager.__version__,
                                                                token=sentinel.token,
                                                                activity=sentinel.activity_id,
                                                                image=sentinel.image_name,
                                                                ovation_cli_args=sentinel.ovation_cli_args))


@patch('paramiko.SSHClient')
@patch('ovation.service.make_session')
def test_submit_research_job_raises_SlurmException_if_submission_fails(make_session, ssh_client):
    s = Mock(spec=session.Session)
    make_session.return_value = (sentinel.token_info, s)

    client = Mock()
    ssh_client.return_value = client

    stdout = Mock()
    stderr = Mock()
    stdout.channel.recv_exit_status.return_value = 1
    stderr.read.return_value = sentinel.job_output
    client.exec_command.return_value = sentinel.stdin, stdout, stderr

    msg = {'activity_id': sentinel.activity_id,
           'organization': sentinel.org,
           'image_name': sentinel.image_name,
           'token': sentinel.token}

    try:
        slurm.submit_research_job(msg,
                                  head_node=sentinel.head_node,
                                  key_filename=sentinel.key_filename)

        assert False, "Should throw exception"

    except slurm.SlurmException as ex:
        assert str(ex) == str(sentinel.job_output)
