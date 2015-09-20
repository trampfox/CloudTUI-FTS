# coding=utf-8

__author__ = 'Davide Monfrecola'

import time
import logging

import ceilometerclient.client

from monitor import Monitor


class OpenstackMonitor(Monitor):
    """Openstack monitoring class via Ceilometer APIs (implements IMonitor interface)"""

    def __init__(self, resources, conf):
        try:
            # TODO capire come gestire le metriche da recuperare
            self.meters = ["cpu_util"]
            self.resources = resources
            self.conf = conf
            self.cclient = ceilometerclient.client.get_client("2",
                                                              os_username=self.conf.ceilometer_username,
                                                              os_password=self.conf.ceilometer_password,
                                                              os_tenant_name=self.conf.ceilometer_tenant_name,
                                                              os_auth_url=self.conf.ceilometer_auth)
            self.signal = True
        except Exception as e:
            logging.error("An error occurred: {0}".format(e.message))
        pass

    def set_stop_signal(self):
        logging.debug("Set signal to False")
        self.signal = False

    def run(self, meters_queue):
        while self.signal:
            logging.info("Monitor thread started")

            for resource in self.resources:
              logging.debug("[OpenStack Monitor] Check resource {0}".format(str(resource["id"])))
                # insert [resource id, value] list into the meters list
                samples = self.get_samples(resource_id=resource["id"], limit=1)
                #### TEST values ####
                '''samples = [
                    {'resource_id': resource["id"],
                     'meter': "cpu_util",
                     'value': randint(80, 150)}
                ]'''
                for sample in samples:
                    # logging.debug("")
                    meters_queue.put(sample)
            # TODO put sleep time in constant file
            time.sleep(5)

    def get_samples(self, resource_id, limit):
        samples = []
        for meter in self.meters:
            query = [
                dict(field='resource_id', op='eq', value=resource_id)
            ]
            # get last sample of meter <meter> for the resource with id <resource_id>
            samples_list = self.cclient.samples.list(meter_name=meter, limit=limit, q=query)

            for sample in samples_list:
                samples.append({
                    "resource_id": sample.resource_id,
                    "meter": meter,
                    "timestamp": sample.timestamp,
                    "value": sample.counter_volume
                })

        return samples

    def stop(self):
        self.set_stop_signal()