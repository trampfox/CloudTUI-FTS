__author__ = 'Davide Monfrecola'

from iruleengine import IRuleEngine
from monitors.sqlitemanager import SqliteConnector
from intellect.Intellect import Intellect
from intellect.Intellect import Callable
from intellect.classes.Resource import Resource


class RuleEngine(IRuleEngine):
    """Rule engine that are used to manage all the rules associated with a cloud manager
       (implements IRuleEngine interface)"""

    def __init__(self):
        self.db = SqliteConnector('samples.db')
        self.resources = {}
        self.my_intellect = Intellect()
        self.read_resources()
        self.read_policies()
        # temp
        #self.db.create("samples", "resource_id text, date text, volume real")

    def read_rules(self):
        pass

    def read_resources(self):
        '''
        reads resources from configuration file and
        creates a new instance of Resource for each
        resource
        '''
        # TODO leggere risorse da file di configurazione yaml
        # test with resource_id = 1
        self.resources['1'] = Resource('1', "Test 1")
        self.my_intellect.learn(self.resources['1'])

    def read_policies(self):
        policy_a = self.my_intellect.learn(Intellect.local_file_uri("intellect/policies/cloudtui.policy"))
        print(policy_a)
        print("cloudtui policy loaded")
        print(self.my_intellect.knowledge)

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

    def run(self, meters_queue):
        while True:
            try:
                element = meters_queue.get()
                print("[RuleEngine] Value received for resource {0:d}: {1:d}"
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
                self.resources[str(element["resource_id"])].add_sample("cpu", element["value"])
                self.my_intellect.reason(["cpu"])

            except Exception, e:
                print("[RuleEngine] Error %s" % e.args[0])

    #def check_policy(self):