__author__ = 'Davide Monfrecola'

import datetime
import monitoringutils
import time

from random import randint
from sqlitemanager import SqliteConnector
from monitor import Monitor

class OpenstackMonitor(Monitor):
    """Openstack monitoring class via Ceilometer APIs (implements IMonitor interface)"""

    def __init__(self, resources):
        try:
            #self.db = SqliteConnector('openstack.db')
            self.resources = resources
        except Exception as e:
            print("An error occurred: {0}".format(e.message))
        pass

    def run(self, meters_queue):
        print(self.resources)
        while True:
            # TODO call celiometer service and get samples for each available resource
            for resource in self.resources:
                print("[OpenstackMonitor] Check resource {0}".format(str(resource["id"])))
                # insert [resource id, value] list into the meters list
                meters_queue.put({'resource_id': resource["id"],
                                  'meter': "cpu_util",
                                  'value': randint(80, 150)})
            time.sleep(3)

#self.resources.append({"id": "6aff697a-f8b3-4f1d-b49b-d2d5077ff2db", "name": 'test-ubuntu'})
