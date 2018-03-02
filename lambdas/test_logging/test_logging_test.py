import unittest
import boto3
from moto import mock_ec2

import test_logging


class TestTestLogging(unittest.TestCase):

  @mock_ec2
  def test_test_logging(self):
    test_logging.aws_work()

if __name__ == "__main__":
  #test_test_logging()
  unittest.main()