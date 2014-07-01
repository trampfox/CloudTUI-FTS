__author__ = 'Davide Monfrecola'

from confmanager import ConfManager
from ConfigParser import SafeConfigParser

class EucalyptusConfManager(ConfManager):
    """Eucalyptus configuration management"""

    def __init__(self):
        ConfManager.__init__(self, 'eucalyptus')
        self.cloud_parser = SafeConfigParser()

    def read(self):
        """Read configuration file"""
        ConfManager.read(self)
        self.read_login_data()

    def read_login_data(self):
        """Read login data from login.txt file"""
        # EC2 #
        self.ec2_access_key_id = self.parser.get('eucalyptus', 'ec2_access_key_id')
        self.ec2_secret_access_key = self.parser.get('eucalyptus', 'ec2_secret_access_key')
        self.ec2_host = self.parser.get('eucalyptus', 'ec2_host')
        self.ec2_port = self.parser.get('eucalyptus', 'ec2_port')
        self.port = self.parser.get('eucalyptus', 'ec2_port')
        self.ec2_path = self.parser.get('eucalyptus', 'ec2_path')
        self.ec2_user_id = self.parser.get('eucalyptus', 'ec2_user_id')

        # S3 #
        self.s3_url = self.parser.get('eucalyptus', 's3_url')
        self.s3_host = self.parser.get('eucalyptus', 's3_host')
        self.s3_port = self.parser.get('eucalyptus', 's3_port')
        self.s3_path = self.parser.get('eucalyptus', 's3_path')

        print("Login data read!")

    def get_repository_host(self):
        return
