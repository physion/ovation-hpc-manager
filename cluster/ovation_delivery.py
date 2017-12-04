import config as config
from google.cloud import pubsub as gc_pubsub
import json
import argparse


def send_result_error(args):
    job_id = args.job_id
    activity = args.activity_id
    error_log = args.error
    print(error_log)
    message = {
        "job_id": job_id,
        "activity": activity,
        "error_log": error_log
    }
    publisher = gc_pubsub.PublisherClient()
    print(config.configuration('GOOGLE_CLOUD_PROJECT_ID'))
    topic_path = publisher.topic_path(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                                      config.configuration('PUBSUB_FAILURES_TOPIC'))

    publisher.publish(topic_path, data=json.dumps(message))
    return "send_result_error"


def send_result_success(args):
    job_id = args.job_id
    activity = args.activity_id
    message = {
        "job_id": job_id,
        "activity": activity,
    }
    publisher = gc_pubsub.PublisherClient()
    topic_path = publisher.topic_path(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                                      config.configuration('PUBSUB_SUCCESSES_TOPIC'))

    publisher.publish(topic_path, data=json.dumps(message))
    return "send_result_success"


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_error = subparsers.add_parser('error', description='Send a error result')
    parser_error.add_argument('-j', '--job_id',  help='Job id')
    parser_error.add_argument('-a', '--activity_id',  help='Activity id')
    parser_error.add_argument('-e', '--error',  help='Error log')
    parser_error.set_defaults(func=send_result_error)

    parser_success = subparsers.add_parser('success', description='Send a success result')
    parser_success.add_argument('-j', '--job_id', help='Job id')
    parser_success.add_argument('-a', '--activity_id', help='Activity id')
    parser_success.set_defaults(func=send_result_success)
    args = parser.parse_args()
    args.func(args)

if __name__ == '__main__':
    main()