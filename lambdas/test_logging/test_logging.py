import sys
#sys.path.append('lib')
import logging
from pythonjsonlogger import jsonlogger
import os
import boto3
import json
import io

service = os.environ.get('SERVICE', 'unknown')
app_tier = os.environ.get('APP_TIER', 'unknown')
log_level = os.environ.get('LOG_LEVEL', 'INFO')


class EntJsonFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        if not log_record.get('service'):
            log_record['service'] = 'unknown'
        if not log_record.get('app_tier'):
            log_record['app_tier'] = 'unknown'
        if not log_record.get('log') and message_dict:
            log_record['log'] = message_dict
            message_dict = {}
        super().add_fields(log_record, record, message_dict)


class LambdaJsonFormatter(EntJsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        if not log_record.get('app_tier'):
            log_record['app_tier'] = app_tier
        if not log_record.get('service'):
            log_record['service'] = service
        super().add_fields(log_record, record, message_dict)

# setup logger
def setup_logger(level='INFO', extras={}):
    extras['service'] = service

    logger = logging.getLogger()
    for h in logger.handlers:
        logger.removeHandler(h)

    format_str = '%(message)%(levelname)%(name)s.%(funcName)s:%(lineno)d%(asctime)'
    formatter = LambdaJsonFormatter(format_str)

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    logger.addHandler(handler)
    logger.setLevel(log_level.upper())
    logger = logging.LoggerAdapter(logger, extras)
    return logger

logger = setup_logger(level=log_level)

def aws_work():
  logger.info({'sns_response': 'response', 'log_msg': 'what'})

  client = boto3.client('ec2', region_name='us-east-1')
  response = client.describe_images(
    Filters=[
        {
            'Name': 'tag:Name',
            'Values': [
                'base-endeca-data-service',
            ]
        },
    ]
  )
  logger.info(response)

def handler(event, context):
    aws_work()

if __name__ == "__main__":
  aws_work()