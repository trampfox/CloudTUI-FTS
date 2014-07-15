__author__ = 'Davide Monfrecola'

import boto
import datetime
from boto.s3.connection import OrdinaryCallingFormat
from boto.s3.connection import S3Connection
from boto.s3.key import Key
from boto.ec2.regioninfo import RegionInfo
from managers.manager import Manager
from confmanager.nimbusconfmanager import NimbusConfManager
from autoscaling.nimbusautoscaling import NimbusAutoScaling

class NimbusManager (Manager):

    def __init__(self):
        self.conf = NimbusConfManager()
        self.conf.read()
        self.conf.read_cloud_conf()
        self.autoscaling = NimbusAutoScaling(self.conf)
        self.images = None
        self.security_groups = None
        self.keys = None
        self.snapshots = None
        self.volumes = None

    def connect(self):
        """Connection to the endpoint specified in the configuration file"""
        try:
            self.region = RegionInfo(name="nimbus", endpoint=self.conf.ec2_host)
            # trying connection to endpoint
            Manager.connect(self)

            print("Connection successfully established: " + self.ec2conn.host)
            print("Connection successfully established (s3conn): " + self.s3conn.host)
        except Exception as e:
            print("Connection error({0})".format(e.message))

    def show_menu(self):
        menu_text = """\nWhat would you like to do?
--------------------------
1) Create new instance
2) Show running instances
3) Reboot instance
4) Terminate instance
5) Select instance to monitor
6) Get CloudWatch metric data
8) Show key pairs
9) Show connection information
10) List autoscaling groups
11) Create autoscaling group
12) List domains
13) Create domain
11) Exit\n"""
        print(menu_text)
        try:
            # user input
            print("Please make a choice: ")
            choice = input()
            if choice == 1:
                self.create_new_instance()
            elif choice == 2:
                self.print_all_instances()
            elif choice == 3:
                self.reboot_instance()
            elif choice == 4:
                self.terminate_instance()
            elif choice == 5:
                self.enable_monitoring()
            elif choice == 6:
                self.get_cloudwatch_metric_data()
            elif choice == 10:
                self.autoscaling.get_launch_configurations()
            elif choice == 11:
                self.autoscaling.create_launch_configuration()
            elif choice == 12:
                self.autoscaling.get_domains()
            elif choice == 13:
                self.autoscaling.create_domain()
            else:
                raise Exception("Unavailable choice!")
        except Exception as e:
            print(e.message)

    def clone_instance(self, instance):
        print("Clone start")
        cf = OrdinaryCallingFormat()

        # get all buckets that user owns
        try:
            buckets = self.s3conn.get_bucket("Repo", validate=False)
        except:
            raise
        # test
        print buckets

    def create_new_instance(self):
        """

        :return:
        """
        Manager.create_new_instance(self)

        # monitoring
        monitoring = raw_input("Do you want to enable monitoring? (y/n): ")
        if monitoring == "y":
            monitoring_enabled = True
        else:
            monitoring_enabled = False

        print("\n--- Creating new instance with the following properties:")
        print("- %-20s %-30s" % ("Image ID", str(self.image_id)))
        print("- %-20s %-30s" % ("Security group", str(self.security_group)))
        print("- %-20s %-30s" % ("Key pair", str(self.key_name)))
        print("- %-20s %-30s" % ("Monitoring", str(monitoring_enabled)))
        #print("\nDo you want to continue? (y/n)")

        try:
            reservation = self.ec2conn.run_instances(image_id=self.image_id,
                                                     key_name=self.key_name,
                                                     security_groups=self.security_group,
                                                     monitoring_enabled=monitoring_enabled,
                                                     min_count=1,
                                                     max_count=1)
            print("\n--- Reservation created")
            print("- %-20s %-30s" % ("ID", reservation.id))
            for instance in reservation.instances:
                print("- %-20s %-30s" % ("Instance ID", instance.id))
                print("- %-20s %-30s" % ("Instance status", instance.state))
                print("- %-20s %-30s" % ("Instance placement", instance.placement))
        except Exception as e:
            print("An error occured: {0}".format(e.message))

    def get_cloudwatch_metric_data(self):
        try:
            instance_id = self.get_instance_id()

            cw_conn = boto.ec2.cloudwatch.CloudWatchConnection(aws_access_key_id=self.conf.ec2_access_key_id,
                                                               aws_secret_access_key=self.conf.ec2_secret_access_key,
                                                               region=self.region,
                                                               validate_certs=False,
                                                               is_secure=False,
                                                               port=8445)

            metrics = cw_conn.list_metrics(dimensions={'InstanceId':[instance_id]})
            metric_statistics = cw_conn.get_metric_statistics(
                60,
                datetime.datetime.utcnow() - datetime.timedelta(seconds=600),
                datetime.datetime.utcnow(),
                'CPUUtilization',
                'AWS/EC2',
                ['Average', 'Sum', 'SampleCount', 'Maximum', 'Minimum'],
                dimensions={'InstanceId':[instance_id]}
            )
            #dimensions={'InstanceId':[instance_id]} --> get_metric_statistics parameter
            print metric_statistics
        except Exception as e:
            print("An error occured: {0}".format(e.message))

    # def clone_instance(self, instance):
    #     """
    #     Make an clone of an existing Instance object.
    #
    #     instance      The Instance object to clone.
    #     """
    #
    #     # TO DO -> the instance selection should be outside of this method
    #     self.print_all_instances()
    #     print("")
    #     vm_index = input("Please select the VM that you want to clone: ")
    #     instance = self.get_instance(vm_index - 1)
    #
    #     new_bdm = None
    #     ec2 = instance.connection
    #     user_data = None
    #
    #     if instance.block_device_mapping:
    #         root_device_name = instance.get_attribute('rootDeviceName')['rootDeviceName']
    #         user_data = instance.get_attribute('userData')['userData']
    #         # user_data comes back base64 encoded.  Need to decode it so it
    #         # can get re-encoded by run_instance !
    #         user_data = base64.b64decode(user_data)
    #         new_bdm = BlockDeviceMapping()
    #
    #         for dev in instance.block_device_mapping:
    #             # if this entry is about the root device, skip it
    #             if dev != root_device_name:
    #                 bdt = instance.block_device_mapping[dev]
    #                 if bdt.volume_id:
    #                     volume = ec2.get_all_volumes([bdt.volume_id])[0]
    #                     snaps = volume.snapshots()
    #                     if len(snaps) == 0:
    #                         print 'No snapshots available for %s' % volume.id
    #                     else:
    #                         # sort the list of snapshots, newest is at the end now
    #                         snaps.sort(key=lambda snap: snap.start_time)
    #                         latest_snap = snaps[-1]
    #                         new_bdt = BlockDeviceType()
    #                         new_bdt.snapshot_id = latest_snap.id
    #                         new_bdm[dev] = new_bdt
    #
    #     return ec2.run_instances(instance.image_id,
    #                              key_name=instance.key_name,
    #                              security_groups=[g.name for g in instance.groups],
    #                              user_data=user_data,
    #                              instance_type=instance.instance_type,
    #                              kernel_id=instance.kernel,
    #                              ramdisk_id=instance.ramdisk,
    #                              monitoring_enabled=instance.monitored,
    #                              placement=instance.placement,
    #                              block_device_map=new_bdm).instances[0]