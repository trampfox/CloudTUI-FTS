__author__ = 'Davide Monfrecola'

from confmanager import ConfManager
from ConfigParser import SafeConfigParser

class NimbusConfManager(ConfManager):
    """nimbus configuration management"""

    def __init__(self):
        ConfManager.__init__(self, 'nimbus')
        self.cloud_parser = SafeConfigParser()

    def read(self):
        """Read configuration file"""
        ConfManager.read(self)
        self.read_login_data()
        self.read_cloud_conf()

    def read_login_data(self):
        """Read login data from login.txt file"""
        self.port = self.parser.get('nimbus', 'port')
        self.path = self.parser.get('nimbus', 'path')
        self.canonical_id = self.parser.get('nimbus', 'canonical_id')
        self.ssh_key_id = self.parser.get('nimbus', 'ssh_key_id')

    def read_cloud_conf(self):
        """Read cloud.properties file"""
        self.cloud_parser.readfp(FakeSecHead(open(self.path + '/conf/hotel.conf')))
        self.ec2_url = self.cloud_parser.get('cloud', 'vws.repository')
        self.ec2_host = self.ec2_url.split(":")[0]
        self.ec2_port = self.ec2_url.split(":")[1]
        self.ec2_access_key_id = self.cloud_parser.get('cloud', 'vws.repository.s3id')
        self.ec2_secret_access_key = self.cloud_parser.get('cloud', 'vws.repository.s3key')
        self.ec2_path = ""

    def get_repository_host(self):
        return



class FakeSecHead(object):
    """Object that add a fake section header. Needed by ConfigParser to read the cloud.properties config file, that has
       no section.
       See: http://stackoverflow.com/questions/2819696/parsing-properties-file-in-python/2819788#2819788"""
    def __init__(self, fp):
        self.fp = fp
        self.sechead = '[cloud]\n'

    def readline(self):
        if self.sechead:
            try:
                return self.sechead
            finally:
                self.sechead = None
        else:
            return self.fp.readline()
