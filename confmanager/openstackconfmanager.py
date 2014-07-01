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
        # boto #
        self.ec2_access_key_id = self.parser.get('openstack', 'ec2_access_key_id')
        self.ec2_secret_access_key = self.parser.get('openstack', 'ec2_secret_access_key')
        self.ec2_url = self.parser.get('openstack', 'ec2_url')
        self.ec2_host = self.parser.get('openstack', 'ec2_host')
        self.ec2_port = self.parser.get('openstack', 'ec2_port')
        self.port = self.parser.get('openstack', 'ec2_port')
        self.ec2_path = self.parser.get('openstack', 'ec2_path')
        self.ec2_private_key = self.parser.get('openstack', 'ec2_private_key')
        self.ec2_cert = self.parser.get('openstack', 'ec2_cert')
        self.nova_cert = self.parser.get('openstack', 'nova_cert')

        self.s3_url = self.parser.get('openstack', 's3_url')
        self.s3_host = self.parser.get('openstack', 's3_host')
        self.s3_port = self.parser.get('openstack', 's3_port')
        # end boto #

        # OpenStack Python SDK #
        self.auth_url = self.parser.get('openstack', 'os_auth_url')
        self.username = self.parser.get('openstack', 'os_username')
        self.api_key = self.parser.get('openstack', 'os_api_key')
        self.tenant_name = self.parser.get('openstack', 'os_tenant_name')

        print("Login data read!")

    def get_repository_host(self):
        return
