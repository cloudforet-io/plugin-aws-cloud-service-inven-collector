import os
import logging

from spaceone.core import utils, config
from spaceone.tester import TestCase, print_json
from google.protobuf.json_format import MessageToDict

_LOGGER = logging.getLogger(__name__)

AKI = os.environ.get('AWS_ACCESS_KEY_ID', None)
SAK = os.environ.get('AWS_SECRET_ACCESS_KEY', None)
ROLE_ARN = os.environ.get('ROLE_ARN', None)
REGION_NAME = os.environ.get('REGION_NAME', None)


if AKI == None or SAK == None:
    print("""
##################################################
# ERROR 
#
# Configure your AWS credential first for test
##################################################
example)

export AWS_ACCESS_KEY_ID=<YOUR_AWS_ACCESS_KEY_ID>
export AWS_SECRET_ACCESS_KEY=<YOUR_AWS_SECRET_ACCESS_KEY>

""")
    exit


class TestCloudServiceAPIs(TestCase):
    config = utils.load_yaml_from_file(
        os.environ.get('SPACEONE_TEST_CONFIG_FILE', './config.yml'))
    endpoints = config.get('ENDPOINTS', {})
    secret_data = {
        'aws_access_key_id': AKI,
        'aws_secret_access_key': SAK,
    }

    if ROLE_ARN is not None:
        secret_data.update({
            'role_arn': ROLE_ARN
        })

    if REGION_NAME is not None:
        secret_data.update({
            'region_name': REGION_NAME
        })

    def test_init(self):
        v_info = self.inventory.Collector.init({'options': {}})
        print_json(v_info)

    def test_verify(self):
        options = {
            'domain': 'mz.co.kr'
        }
        v_info = self.inventory.Collector.verify({'options': options, 'secret_data': self.secret_data})
        print_json(v_info)

    def test_collect(self):
        options = {}
        filter = {}

        res_stream = self.inventory.Collector.collect(
            {'options': options, 'secret_data': self.secret_data, 'filter': filter}
        )

        for res in res_stream:
            self.assertIsNotNone(res)
            print_json(res)
            # self.assertEqual('CLOUD_SERVICE', res.resource_type)
