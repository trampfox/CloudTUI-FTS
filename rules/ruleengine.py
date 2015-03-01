__author__ = 'Davide Monfrecola'

from iruleengine import IRuleEngine
from monitors.sqlitemanager import SqliteConnector
from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from intellect.classes.Resource import Resource

import sys
import os

class RuleEngine(IRuleEngine):
    """Rule engine that are used to manage all the rules associated with a cloud manager
       (implements IRuleEngine interface)"""

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

    def read_policies(self):
        policy_a = self.my_intellect.learn(Intellect.local_file_uri("intellect/policies/openstack.policy"))
        print("[RuleEngine] Openstack policy loaded")
        # TEST
        self.agenda_groups.append("cpu")
        self.agenda_groups.append("network")

    def run(self, meters_queue):
        self.init_resources()
        self.read_policies()
        while True:
            try:
                element = meters_queue.get()
                print("[RuleEngine] Value received for resource {0}: {1}"
                       .format(element["resource_id"], element["value"]))
                '''last_value = self.get_last_value(element["resource_id"])
                last_value = self.get_last_value(element["resource_id"])
                if last_value is None:
                    print("Insert first record")
                    self.db.insert("samples",
                                   "'{0}', '{1}', '{2}'".format(element["resource_id"],
                                                          datetime.now(),
                                                          element["value"]))
                else:
                    print("Update record")
                    ema_value = monitoringutils.ema(element["value"], last_value)
                    self.db.update("samples",
                                   "volume='{0:.3f}'".format(ema_value),
                                   "resource_id='{0}'".format(element["resource_id"]))
                '''
                self.resources[element["resource_id"]].add_sample(element["meter"], element["value"])
                #self.resources[element["resource_id"]].add_sample("cpu", element["value"])

                self.check_policies()

            except Exception, e:
                print("[RuleEngine] Error %s" % e.args[0])
                print(sys.exc_info()[0].__name__)
                print(os.path.basename(sys.exc_info()[2].tb_frame.f_code.co_filename))
                print(sys.exc_info()[2].tb_lineno)

    def check_policies(self):
        self.my_intellect.reason(self.agenda_groups)


    '''def get_last_value_test(self, resource_id):
        #Checks if is the first value for the resorce with the ID specified
        self.db.connect()

        value = None
        rows = self.db.query("SELECT * FROM samples WHERE resource_id='{0}' LIMIT 1".format(resource_id))
        # debug

        for row in rows:
            print("Rows found")
            print row
            value = row[2]

        return value'''
