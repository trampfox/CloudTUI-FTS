from cloudtui.cloudtui import CloudTUI
from managers.manager import Manager

__author__ = 'Davide Monfrecola'

import managers
import os
import boto
import sys
import signal
import threading
import string
import socket
import subprocess
import time
import cloudtui

from clonevm import VM      # TODO choose where to put the VM class
from confmanager.nimbusconfmanager import NimbusConfManager
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
#from ssl import SSLSocket
#from phantomclient.phantomclient import PhantomClient
#from phantomclient.phantomrequest import PhantomRequest
from monitors.openstackmonitor import OpenstackMonitor
from rules.ruleengine import RuleEngine
from managers.openstack.openstackagent import OpenstackAgent
from managers.openstack.openstackmanager import OpenstackManager
from Queue import Queue
from threading import Thread


def signal_handler(signal, frame):
    print('You pressed Ctrl+C!')
    sys.exit(0)

if __name__ == "__main__":
    #pr = PhantomRequest()
    #pr.test()
    '''cloudTUI = CloudTUI()
    cloudTUI.start()'''
    meters_queue = Queue()
    cmd_queue = Queue()

    os_manager = OpenstackManager()
    os_manager.connect()
    resources = os_manager.get_instance_info()

    os_monitor = OpenstackMonitor(resources)
    monitor = Thread(target=os_monitor.run, args=(meters_queue,))
    monitor.setDaemon(True)
    monitor.start()

    rule_engine = RuleEngine(resources, cmd_queue)
    rule_engine_monitor = Thread(target=rule_engine.run, args=(meters_queue,))
    rule_engine_monitor.setDaemon(True)
    rule_engine_monitor.start()

    agent = OpenstackAgent()
    os_agent = Thread(target=agent.run, args=(cmd_queue,))
    os_agent.setDaemon(True)
    os_agent.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.pause()

    raw_input("Please enter to exit")
