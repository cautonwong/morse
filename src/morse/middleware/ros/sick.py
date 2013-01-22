import logging; logger = logging.getLogger("morse." + __name__)
import roslib; roslib.load_manifest('sensor_msgs')
import math
from sensor_msgs.msg import LaserScan
from sensor_msgs.msg import PointCloud

def init_extra_module(self, component_instance, function, mw_data):
    """ Setup the middleware connection with this data

    Prepare the middleware to handle the serialised data as necessary.
    """
    component_instance.output_functions.append(function)
    topic = mw_data[3].get("topic", self.get_topic_name(component_instance))
    self.set_topic_name(component_instance, topic)
    self.register_publisher_name_class(topic, get_ros_class(mw_data[1]))

def get_ros_class(method_name):
    dict_method_class = {
        'post_2DLaserScan': LaserScan,
        'post_2DPointCloud': PointCloud,
    }
    return dict_method_class[method_name]

def post_2DLaserScan(self, component_instance):
    """ Publish the data on the rostopic """
    laserscan = LaserScan()
    laserscan.header = self.get_ros_header(component_instance)
    laserscan.header.frame_id = '/base_laser_link'

    # Note: Scan time and laser frequency are chosen as standard values
    laser_frequency = 40 # TODO ? component_instance.frequency()
    scan_window = component_instance.bge_object['scan_window']
    num_readings = scan_window / component_instance.bge_object['resolution']

    laserscan.angle_max = scan_window * math.pi / 360
    laserscan.angle_min = laserscan.angle_max * -1
    laserscan.angle_increment = scan_window / num_readings * math.pi / 180
    laserscan.time_increment = 1 / laser_frequency / num_readings
    laserscan.scan_time = 1.0
    laserscan.range_min = 0.3
    laserscan.range_max = component_instance.bge_object['laser_range']
    laserscan.ranges = component_instance.local_data['range_list']

    self.publish(laserscan, component_instance)

#WARNING: posting 2D-Pointclouds does NOT work at the moment due to Python3 encoding errors
def post_2DPointCloud(self, component_instance):
    """ Publish the data on the rostopic """
    pointcloud = PointCloud()
    pointcloud.header = self.get_ros_header(component_instance)
    pointcloud.header.frame_id = '/base_laser_link'

    pointcloud.points = component_instance.local_data['point_list']

    self.publish(pointcloud, component_instance)
