__author__ = 'Davide Monfrecola'

import boto
import datetime
import boto.ec2.cloudwatch
import monitoringutils
import time

from random import randint
from sqlitemanager import SqliteConnector
from monitor import Monitor

class OpenstackMonitor(Monitor):
    """Openstack monitoring class via Ceilometer APIs (implements IMonitor interface)"""

    def __init__(self):
        try:
            self.db = SqliteConnector('openstack.db')
            # TODO lettura delle risorse da file yaml
            self.resources = []
            self.resources.append({"id": "1", "name": 'test', "meters": ["cpu", "network"]})
        except Exception as e:
            print("An error occurred: {0}".format(e.message))
        pass

    def run(self, meters_queue):
        while True:
            # TODO call celiometer service and get samples for each available resource
            for resource in self.resources:
                print("Check resource ")
                print(resource["id"])
                # insert [resource id, value] list into the meters list
                meters_queue.put({'resource_id': 1, 'value': randint(80, 150)})
            time.sleep(2)

    def get_statistics(self, resource_id):
        pass

    def get_samples(self):
        pass

    def get_last_ema(self):
        pass