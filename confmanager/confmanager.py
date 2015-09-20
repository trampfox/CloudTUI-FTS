__author__ = 'Davide Monfrecola'

from ConfigParser import SafeConfigParser

class ConfManager():
    """Common base class for all configuration manager"""

    def __init__(self, platform):
        """Initialize parser object"""
        print('Configuring CloudTUI components...')
        self.__platform = platform
        self.parser = SafeConfigParser()
        self.parser.read('conf/' + self.__platform + '/login.conf')

    def read(self):
        """Read configuration file"""
        self.read_options()

    def read_login_data(self):
        """Read login data from login.txt file"""
        pass

    def read_monitor_data(self):
        """Read monitor configuration data from login.txt file"""
        self.monitor_port = self.parser.get('monitor', 'port')
        self.monitor_host = self.parser.get('monitor', 'host')
        self.monitor_enabled = self.parser.get('monitor', 'enabled')

    def read_options(self):
        """Read options values from [option] section"""
        if (self.parser.has_option('options', 'validate_certs')):
          self.validate_certs = self.parser.get('options', 'validate_certs')
        if (self.parser.has_option('options', 'terminal')):
          self.terminal = self.parser.get('options', 'terminal')
        else:
          self.terminal = "default"
