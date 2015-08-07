__author__ = 'Davide Monfrecola'

from confmanager import ConfManager
from ConfigParser import SafeConfigParser

class OpenstackConfManager(ConfManager):
    """OpenStack configuration management"""

    def __init__(self):
        ConfManager.__init__(self, 'openstack')
        self.cloud_parser = SafeConfigParser()

    def read(self):
        """Read configuration file"""
        ConfManager.read(self)
        self.read_login_data()

    def read_login_data(self):
        """Read login data from login.txt file"""
        # OpenStack Python SDK #
        self.auth_url = self.parser.get('openstack', 'os_auth_url')
        self.username = self.parser.get('openstack', 'os_username')
        self.password = self.parser.get('openstack', 'os_password')
        #self.api_key = self.parser.get('openstack', 'os_api_key')
        self.tenant_name = self.parser.get('openstack', 'os_tenant_name')

        # OpenStack Ceilometer
        self.ceilometer_auth = self.parser.get('openstack', 'os_ceilometer_auth')
        self.ceilometer_username = self.parser.get('openstack', 'os_ceilometer_username')
        self.ceilometer_password = self.parser.get('openstack', 'os_ceilometer_password')
        self.ceilometer_tenant_name = self.parser.get('openstack', 'os_ceilometer_tenant_name')

        if self.auth_url == "":
            self.get_auth_url()

        #print("Login data read!")

    def get_auth_url(self):
        self.auth_url = raw_input("Please insert auth url: ")