import logging

__author__ = 'Davide Monfrecola'

from monitors.sqlitemanager import SqliteConnector
from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from intellect.classes.Resource import Resource

import sys
import os

class RuleEngine():
    """Rule engine that are used to manage all the rules associated with a
       cloud manager"""

    def __init__(self, resources, cmd_queue):
        self.cmd_queue = cmd_queue
        self.resource_info = resources
        self.resources = {}
        self.my_intellect = Intellect()
        self.agenda_groups = []
        self.signal = True

    def init_resources(self):
        '''
        creates a new instance of Resource for each
        resource in self.resources
        '''
        logging.debug("Initializing rule engine resources")
        for resource in self.resource_info:
            self.resources[resource['id']] = Resource(resource_id=resource["id"],
                                                      name=resource["name"],
                                                      command_queue=self.cmd_queue)
            logging.info("Add resource {0} as fact".format(resource["name"]))
            self.my_intellect.learn(self.resources[resource['id']])

    def add_instance(self, resource):
        self.resources[resource['id']] = Resource(resource_id=resource["id"],
                                                  name=resource["name"],
                                                  command_queue=self.cmd_queue)
        logging.info("Add resource {0} as fact".format(resource["name"]))
        self.my_intellect.learn(self.resources[resource['id']])


    def read_policies(self):
        self.my_intellect.learn(Intellect.local_file_uri("intellect/policies/openstack.policy"))
        logging.info("Openstack policy loaded")
        # TEST
        # TODO gestione agenda groups
        self.agenda_groups.append("cpu")
        self.agenda_groups.append("network")

    def run(self, meters_queue):
        self.init_resources()
        self.read_policies()
        logging.info("Rule engine initialization completed")

        while self.signal:
            try:
                element = meters_queue.get()
                logging.info("[RuleEngine] Value received for resource {0}".format(str(element)))
                logging.debug("Add sample: {0}".format(element))

                self.resources[element["resource_id"]].add_sample(meter=element["meter"],
                                                                  value=element["value"],
                                                                  timestamp=element["timestamp"])

                self.check_policies()

            except Exception, e:
                logging.error("An error occured: %s" % e.args[0])

    def check_policies(self):
        logging.debug("Check policies (call reason method)")
        self.my_intellect.reason(self.agenda_groups)

    def set_stop_signal(self):
        self.signal = False

    def stop(self):
        self.set_stop_signal()