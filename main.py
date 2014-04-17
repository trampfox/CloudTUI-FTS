from cloudtui.cloudtui import CloudTUI
from managers.Manager import Manager

__author__ = 'Davide Monfrecola'

import managers
import os
import boto
import sys
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
#from ssl import SSLSocket
import threading
import string
import socket
import subprocess
from clonevm import VM      # TODO choose where to put the VM class
import time
import cloudtui

def hello():
    print("Hello world")


if __name__ == "__main__":
    cloudTUI = CloudTUI()
    cloudTUI.start()
