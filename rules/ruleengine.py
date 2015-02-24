__author__ = 'Davide Monfrecola'

from monitors import monitoringutils
from iruleengine import IRuleEngine
from rule import Rule
from monitors.sqlitemanager import SqliteConnector
from datetime import datetime
from monitors.intellect.Intellect import Intellect
from monitors.intellect.Intellect import Callable
from monitors.intellect.examples.testing.ClassA import ClassA

class RuleEngine(IRuleEngine):
    """Rule engine that are used to manage all the rules associated with a cloud manager
       (implements IRuleEngine interface)"""

    def __init__(self):
        self.db = SqliteConnector('samples.db')
        # temp
        #self.db.create("samples", "resource_id text, date text, volume real")

    def read_rules(self):
        pass

    def get_last_value(self, resource_id):
        ''' Checks if is the first value for the resorce with the ID specified '''
        self.db.connect()

        value = None
        rows = self.db.query("SELECT * FROM samples WHERE resource_id='{0}' LIMIT 1".format(resource_id))
        # debug

        for row in rows:
            print("Rows found")
            print row
            value = row[2]

        return value

    def run(self, meters_queue):
        while True:
            try:
                element = meters_queue.get()
                print("[RuleEngine] Value received for resource {0:d}: {1:d}"
                       .format(element["resource_id"], element["value"]))
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

                self.db.print_all("samples")

            except Exception, e:
                print("Error %s:" % e.args[0])

    #def check_policy(self):