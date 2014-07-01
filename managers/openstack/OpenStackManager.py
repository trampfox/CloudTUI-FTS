__author__ = 'Davide Monfrecola'

import boto
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.regioninfo import RegionInfo
from managers.manager import Manager
from confmanager.openstackconfmanager import OpenstackConfManager
import novaclient.v1_1.client as nvclient

class OpenStackManager(Manager):
    
    def __init__(self):
        self.conf = OpenstackConfManager()
        self.conf.read()

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        """try:
            # boto #
            self.region = RegionInfo(name="nova", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            Manager.connect(self)
            # end boto #

            print("Connection successfully established")
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))"""

        # OpenStack Python SDK #
        try:
            self.nova = nvclient.Client(auth_url=self.conf.auth_url,
                                        username=self.conf.username,
                                        api_key=self.conf.api_key,
                                        project_id=self.conf.tenant_name)

            print("Connection successfully established ")
            #print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

        # end OpenStack Python SDK #

    def print_all_instances(self):
        print self.ec2conn.get_all_regions()

    def print_all_instances(self):
        print("Retrieving all instances...")
        print self.nova.servers.list()

    def print_all_images(self):
        print("Retrieving all images...")
        print self.nova.images.list()