__author__ = 'Davide Monfrecola'

from confmanager import ConfManager
from ConfigParser import SafeConfigParser, NoOptionError


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
        try:
            self.auth_url = self.parser.get('openstack', 'os_auth_url')
        except NoOptionError:
            self.get_auth_url()
        try:
            self.username = self.parser.get('openstack', 'os_username')
        except NoOptionError:
            self.get_username()
        try:
            self.password = self.parser.get('openstack', 'os_password')
        except NoOptionError:
            self.get_password()
        #self.api_key = self.parser.get('openstack', 'os_api_key')
        try:
            self.tenant_name = self.parser.get('openstack', 'os_tenant_name')
        except NoOptionError:
            self.get_tenant_name()

        # OpenStack Ceilometer
        self.ceilometer_auth = self.parser.get('openstack', 'os_ceilometer_auth')
        self.ceilometer_username = self.parser.get('openstack', 'os_ceilometer_username')
        self.ceilometer_password = self.parser.get('openstack', 'os_ceilometer_password')
        self.ceilometer_tenant_name = self.parser.get('openstack', 'os_ceilometer_tenant_name')
        #print("Login data read!")

    def get_auth_url(self):
        print("## Auth URL not found in configuration")
        print("-- Please insert auth url: ")
        self.auth_url = raw_input("--> ")
        print("")

    def get_username(self):
        print("## Username not found in configuration")
        print("-- Please insert username: ")
        self.username = raw_input("--> ")
        print("")

    def get_password(self):
        print("## Password not found in configuration")
        print("-- Please insert password: ")
        self.password = raw_input("--> ")
        print("")

    def get_tenant_name(self):
        print("## Tenant name not found in configuration")
        print("-- Please insert tenant name: ")
        self.tenant_name = raw_input("--> ")
        print("")
