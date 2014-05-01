__author__ = 'Davide Monfrecola'

from confmanager import ConfManager

class NimbusConfManager(ConfManager):
    """nimbus configuration management"""

    def __init__(self):
        ConfManager.__init__(self, 'nimbus')

    def read_login_data(self):
        """Read login data from login.txt file"""
        self.port = self.parser.get('nimbus', 'port')
        self.path = self.parser.get('nimbus', 'path')
        self.canonical_id = self.parser.get('nimbus', 'canonical_id')
        self.ssh_key_id = self.parser.get('nimbus', 'ssh_key_id')

