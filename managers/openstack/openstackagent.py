__author__ = 'Davide Monfrecola'

from managers.openstack.openstackmanager import OpenstackManager

import logging

class OpenstackAgent:

    def __init__(self):
        self.manager = OpenstackManager()
        self.manager.connect()

    def run(self, cmd_queue):
        while True:
            try:
                command = cmd_queue.get()
                print("[Openstack agent] Command received: " + str(command))

                self.execute_command(command)
            except Exception, e:
                print("Error %s:" % e.args[0])

    def execute_command(self, command):
        if(command['command'] == "clone"):
            self.manager.clone_instance(command['resource_id'])
