__author__ = 'Davide Monfrecola'

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.ec2.regioninfo import RegionInfo
from managers.manager import Manager
from confmanager.nimbusconfmanager import NimbusConfManager

class NimbusManager (Manager):

    def __init__(self):
        self.conf = NimbusConfManager()
        self.conf.read()

        print("Instance of class", NimbusManager.__name__)

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        try:
            self.region = RegionInfo(name="nimbus", endpoint=self.conf.vws_repository_host)
            # trying connection to endpoint
            Manager.connect(self)

            print("Connection successfully established: " + self.ec2conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))
