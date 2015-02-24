__author__ = 'Davide Monfrecola'

import logging

class OpenstackAgent:

    def __init__(self):
        print("[Openstack agent] Started")

    def run(self, cmd_queue):
        while True:
            try:
                command = cmd_queue.get()
                print("[Openstack agent] Command received: " + command)
            except Exception, e:
                print("Error %s:" % e.args[0])
