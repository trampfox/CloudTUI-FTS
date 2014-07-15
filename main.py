from cloudtui.cloudtui import CloudTUI
from managers.manager import Manager

__author__ = 'Davide Monfrecola'

import managers
import os
import boto
import sys
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
from phantomclient.phantomclient import PhantomClient
from phantomclient.phantomrequest import PhantomRequest

def hello():
    print("Hello world")


if __name__ == "__main__":
    pr = PhantomRequest()
    pr.test()
    #cloudTUI = CloudTUI()
    #cloudTUI.start()
