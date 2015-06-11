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

    def init_resources(self):
        '''
        creates a new instance of Resource for each
        resource in self.resources
        '''
        for resource in self.resource_info:
            self.resources[resource['id']] = Resource(resource_id=resource["id"],
                                                      name=resource["name"],
                                                      command_queue=self.cmd_queue)
            print("[RuleEngine] Add resource {0} as fact".format(resource["name"]))
            self.my_intellect.learn(self.resources[resource['id']])

    def add_instance(self, resource):
        self.resources[resource['id']] = Resource(resource_id=resource["id"],
                                                  name=resource["name"],
                                                  command_queue=self.cmd_queue)
        print("[RuleEngine] Add resource {0} as fact".format(resource["name"]))
        self.my_intellect.learn(self.resources[resource['id']])


    def read_policies(self):
        policy_a = self.my_intellect.learn(Intellect.local_file_uri("intellect/policies/openstack.policy"))
        #print("[RuleEngine] Openstack policy loaded")
        # TEST
        # TODO gestione agenda groups
        self.agenda_groups.append("cpu")
        self.agenda_groups.append("network")

    def run(self, meters_queue):
        self.init_resources()
        self.read_policies()
        while True:
            try:
                element = meters_queue.get()
                print("[RuleEngine] Value received for resource {0}"
                       .format(str(element)))

                self.resources[element["resource_id"]].add_sample(meter=element["meter"],
                                                                  value=element["value"],
                                                                  timestamp=element["timestamp"])

                self.check_policies()

            except Exception, e:
                print("[RuleEngine] Error %s" % e.args[0])
                print(sys.exc_info()[0].__name__)
                print(os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename))
                print(sys.exc_info()[2].tb_lineno)

    def check_policies(self):
        self.my_intellect.reason(self.agenda_groups)
