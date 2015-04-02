__author__ = 'Davide Monfrecola'

from confmanager import ConfManager
from ConfigParser import SafeConfigParser

class RuleEngineConfManager(ConfManager):
    """RuleEngine configuration management"""

    def __init__(self):
        ConfManager.__init__(self, 'ruleengine')
        self.cloud_parser = SafeConfigParser()

    def read(self):
        """Read configuration file"""
        ConfManager.read(self)
        self.read_login_data()

    def read_login_data(self):
        """Read login data from login.txt file"""
        # boto #
        # TODO adattare a ruleengine/conf.txt
        print("Login data read!")

    def get_repository_host(self):
        return
