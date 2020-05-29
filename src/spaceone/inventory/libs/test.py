import logging
from functools import partial

from spaceone.core.transaction import Transaction
from spaceone.tester import TestCase

from .connector import SchematicAWSConnector, get_session

_LOGGER = logging.getLogger(__name__)


class BaseConnectorTestCase(TestCase):
    credentials = {
        'aws_access_key_id': '',
        'aws_secret_access_key': '',
        'region': 'ap-northeast-2'
    }

    connector_class: SchematicAWSConnector = None
    connector_config = {}
    connector_options = {}
    connector_kwargs = {}

    moto_mock = []
    _session = None

    def init_property(self, name: str, init_data: callable):
        if self.__getattribute__(name) is None:
            self.__setattr__(name, init_data())
        return self.__getattribute__(name)

    @property
    def session(self):
        return self.init_property('_session', partial(get_session, self.credentials))

    def setUp(self):
        self.set_up_moto()
        self.connector = self.connector_class(
            Transaction(), self.connector_config, self.connector_options,
            credentials=self.credentials, **self.connector_kwargs)

    def tearDown(self):
        self.tear_down_moto()

    def set_up_moto(self):
        for mock in self.moto_mock:
            mock.start()

    def tear_down_moto(self):
        for mock in self.moto_mock:
            mock.stop()

    def assertCloudServiceTypeRequiredField(self, resp) -> None:
        self.assertEqual(resp.resource_type, 'CLOUD_SERVICE_TYPE')
        self.assertTrue(resp.resource.get('name'))
        self.assertTrue(resp.resource.get('provider'))
        self.assertTrue(resp.resource.get('group'))
        self.assertGreaterEqual(1, len(resp.match_rules))

    def assertCloudServiceRequiredField(self, resp):
        self.assertEqual(resp.resource_type, 'CLOUD_SERVICE')
        self.assertTrue(resp.resource.get('cloud_service_type'))
        self.assertTrue(resp.resource.get('cloud_service_group'))
        self.assertTrue(resp.resource.get('provider'))
        self.assertGreaterEqual(1, len(resp.match_rules))

        def check_rule(rules):
            return all([x in rules for x in ('provider', 'cloud_service_type', 'cloud_service_group')])

        self.assertTrue(any([check_rule(rules) for rules in resp.match_rules.values()]))
