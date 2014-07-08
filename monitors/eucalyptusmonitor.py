__author__ = 'Davide Monfrecola'

import boto
import datetime
import boto.ec2.cloudwatch
from monitor import Monitor

class EucalyptusMonitor(Monitor):
    """Common base class for all cloud platform monitor (implements IMonitor interface)"""

    def __init__(self):
        pass


