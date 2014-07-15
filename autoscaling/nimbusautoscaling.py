__author__ = 'Davide Monfrecola'

import boto
import sys
import datetime
import boto.ec2.autoscale
from boto.ec2.autoscale import Tag
from autoscaling import AutoScaling
from boto.regioninfo import RegionInfo

class NimbusAutoScaling(AutoScaling):
    """"""

    def __init__(self, conf):
        self.conf = conf
        self.connect()

    def connect(self):
        region = RegionInfo(name="nimbus", endpoint=self.conf.phantom_host)
        try:
            self.conn = boto.ec2.autoscale.AutoScaleConnection(self.conf.ec2_access_key_id,
                                                               self.conf.ec2_secret_access_key,
                                                               is_secure=False,
                                                               port=int(self.conf.phantom_port),
                                                               debug=2,
                                                               region=region,
                                                               validate_certs=False)
            self.conn.host = self.conf.phantom_host
        except Exception as e:
            print("Connection error: {0}".format(e.message))


    def get_launch_configurations(self):
        launch_confs = self.conn.get_all_launch_configurations()

        for lc in launch_confs:
            print lc

    def create_launch_configuration(self):
        name="test@hotel"
        image_id="hello-cloud"
        key_name="phantomkey"
        it="m1.small"

        lc = boto.ec2.autoscale.launchconfig.LaunchConfiguration(self.conn, name=name, image_id=image_id, key_name=key_name, security_groups=['default'], instance_type=it,)

        try:
            x = self.conn.create_launch_configuration(lc)
            print x
        except Exception as e:
            print("error lc: {0}".format(e.error_message))

    def get_domains(self):
        domains = self.conn.get_all_groups()

        for domain in domains:
            print domain.name

    def create_domain(self):
        name="testDomain1"
        lc_name="test@hotel"
        n_preserve=1

        policy_name_key = 'PHANTOM_DEFINITION'
        policy_name = 'error_overflow_n_preserving'
        ordered_clouds_key = 'clouds'
        ordered_clouds = ""
        delim = ""
        #qui nello script passa il numero di istanze per ogni cloud disponbile. io provo solo su hotel
        for cloud_size in ["hotel:1"]:
            (cloudname, maxsize) = cloud_size.split(':')
            ordered_clouds = ordered_clouds + delim + cloud_size
            delim = ","

        n_preserve_key = 'minimum_vms'

        # make the tags
        policy_tag = Tag(connection=self.conn, key=policy_name_key, value=policy_name, resource_id=name)
        clouds_tag = Tag(connection=self.conn, key=ordered_clouds_key, value=ordered_clouds, resource_id=name)
        npreserve_tag = Tag(connection=self.conn, key=n_preserve_key, value=n_preserve, resource_id=name)

        tags = [policy_tag, clouds_tag, npreserve_tag]

        lc_a = x = self.conn.get_all_launch_configurations(names=[lc_name,])
        if not lc_a:
            print "No such launch configuration"
            sys.exit(1)
        lc = lc_a[0]
        print 'using %s' % (str(lc))
        asg = boto.ec2.autoscale.group.AutoScalingGroup(connection=self.conn, group_name=name, availability_zones=["us-east-1"], min_size=n_preserve, max_size=n_preserve, launch_config=lc, tags=tags)

        try:
            self.conn.create_auto_scaling_group(asg)
            print x
        except Exception as e:
            print("Create domain error: {0}".format(e.message))