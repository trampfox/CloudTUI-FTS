__author__ = 'Davide Monfrecola'

class IConfManager:
    """This interface defines all the methods that a configuration manager class must implement """

    def read_login_data(self):
        """Read login data from login.txt file"""
        raise NotImplementedError

    def read_monitor_data(self):
        """Read monitor configuration data from login.txt file"""
        raise NotImplementedError

    def read_options(self):
        """Read options values from [option] section"""
        raise NotImplementedError