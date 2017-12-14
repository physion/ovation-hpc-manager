import config as config
from google.cloud import pubsub as gc_pubsub
import json
import argparse
import logging
import sys
import os

level = logging.DEBUG if 'DEBUG_LOG' in os.environ else logging.INFO
logging.basicConfig(stream=sys.stdout, level=level)


def send_result(**args):
    message = {}
    topic = args.get('topic')

    message['job_id'] = args.get('job_id')
    message['activity_id'] = args.get('activity_id')
    if args.get('error_log') is not None: message['error_log'] = args.get('error_log')

    data = json.dumps(message)
    data = data.encode('utf-8')

    publisher = gc_pubsub.PublisherClient()
    topic_path = publisher.topic_path(config.configuration('GOOGLE_CLOUD_PROJECT_ID'),
                                      topic)

    publisher.publish(topic_path, data=data)
    logging.info("The message sent to the topic {} is: {}".format(topic, json.dumps(message)))


def main():
    parser = argparse.ArgumentParser()
    subparsers = parser.add_subparsers()
    parser_error = subparsers.add_parser('error', description='Send a error result')
    parser_error.add_argument('-j', '--job_id', help='Job id')
    parser_error.add_argument('-a', '--activity_id', help='Activity id')
    parser_error.add_argument('-e', '--error', help='Error log')
    parser_error.set_defaults(topic=config.configuration('PUBSUB_FAILURES_TOPIC'))

    parser_success = subparsers.add_parser('success', description='Send a success result')
    parser_success.add_argument('-j', '--job_id', help='Job id')
    parser_success.add_argument('-a', '--activity_id', help='Activity id')
    parser_success.set_defaults(topic=config.configuration('PUBSUB_SUCCESSES_TOPIC'))

    args = parser.parse_args()
    send_result(topic=args.topic, job_id=args.job_id, activity_id=args.activity_id, error_log=args.error)


if __name__ == '__main__':
    sys.exit(main())
