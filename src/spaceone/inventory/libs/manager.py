from spaceone.core.manager import BaseManager


class AWSManager(BaseManager):
    connector_name = None

    def verify(self, options, secret_data, **kwargs):
        """ Check collector's status.
        """
        connector = self.locator.get_connector(self.connector_name, secret_data=secret_data)
        connector.verify()

    def collect_resources(self, **kwargs) -> list:
        return self.locator.get_connector(self.connector_name, **kwargs).collect_data()
