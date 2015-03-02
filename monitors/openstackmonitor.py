# coding=utf-8

__author__ = 'Davide Monfrecola'

import datetime
import monitoringutils
import time
import ceilometerclient.client

from random import randint
from sqlitemanager import SqliteConnector
from monitor import Monitor
from confmanager.openstackconfmanager import OpenstackConfManager


class OpenstackMonitor(Monitor):
    """Openstack monitoring class via Ceilometer APIs (implements IMonitor interface)"""

    def __init__(self, resources):
        try:
            self.resources = resources
            self.conf = OpenstackConfManager()
            self.conf.read()
            self.cclient = ceilometerclient.client.get_client(2,
                                                              os_username=self.conf["os_ceilometer_username"],
                                                              os_password=self.conf["os_ceilometer_password"],
                                                              os_tenant_name=self.conf["os_ceilometer_tenant_name"],
                                                              os_auth_url=self.conf["os_ceilometer_auth"])
            # TODO capire come gestire le metriche da recuperare
            self.meters = ["cpu_util"]
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
                samples = self.get_samples(resource_id=resource["id"])
                #### TEST values ####
                samples = [
                    {'resource_id': resource["id"],
                     'meter': "cpu_util",
                     'value': randint(80, 150)}
                ]
                for sample in samples:
                    meters_queue.put(sample)
            time.sleep(3)

    def get_samples(self, resource_id):
        for meter in self.meters:
            query = [
                dict(field='resource_id', op='eq', value=resource_id)
            ]
            # get last sample of meter <meter> for the resource with id <resource_id>
            sample = self.cclient.samples.list(meter_name=meter, limit=1, q=query)
            #print(str(sample))
            # TODO vedere che cosa ci può essere di interessante tra le statistiche
            statistics = self.cclient.statistics(meter_name=meter, q=query)
            print(str(statistics))
