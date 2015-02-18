__author__ = 'Davide Monfrecola'

import boto
import datetime
import boto.ec2.cloudwatch
from monitors import Monitor

class OpenstackMonitor(Monitor):
    """Openstack monitoring class via Ceilometer APIs (implements IMonitor interface)"""

    def __init__(self):
        pass

    def get_statistics(self):
        pass

    #def get_

