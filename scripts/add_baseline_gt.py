#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy
from manhole_detector.msg import Manhole
from geometry_msgs.msg import PoseStamped
import numpy as np
from math import floor
from sensor_msgs.msg import CompressedImage

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <baseline_file> [<gt_file> <graph_file>]'.format(sys.argv[0])
  sys.exit(-1)
baseline_topic = "/baseline"
alt_baseline_topic = "/visual_odometry"
ground_truth_topic = "/manhole"
image_topic = "/up/depth_registered/image_raw/compressedDepth"
# if (len(sys.argv) > 3):
#   new_topic = sys.argv[4]

# temp_delta = sys.argv[3]

baseline_matrix = np.loadtxt(sys.argv[3])
if sys.argv > 4:
    ground_truth_matrix = np.loadtxt(sys.argv[4])
    graph_matrix = np.loadtxt(sys.argv[5])
    ground_truth = True
else:
    ground_truth = False

cont_alt_baseline = 0
cont_baseline = 0
cont_gt = 0
print "Opening {0}".format(sys.argv[1])
bag = rosbag.Bag(sys.argv[1])
total = bag.get_message_count()
print 'Total messages: ',total
cont = 0
with rosbag.Bag(sys.argv[2], 'w') as outbag:
  for topic, msg, t in bag.read_messages():
    time_float = t.secs + t.nsecs * 1e-9
    # print time_float
    # if cont_baseline < curr_row:
        # print baseline_matrix[cont_baseline][8]
    if topic == baseline_topic:
      cont_alt_baseline += 1
      outbag.write(alt_baseline_topic, msg, t)
    elif cont_baseline < len(baseline_matrix) and time_float > baseline_matrix[cont_baseline][8]:
        new_msg = PoseStamped()
        new_msg.header.frame_id = "/map"
        new_msg.header.stamp.secs = floor(baseline_matrix[cont_baseline][8])
        new_msg.header.stamp.nsecs = (baseline_matrix[cont_baseline][8] - new_msg.header.stamp.secs)*1e9
        new_msg.pose.position.x = baseline_matrix[cont_baseline][0]
        new_msg.pose.position.y = baseline_matrix[cont_baseline][1]
        new_msg.pose.position.z = baseline_matrix[cont_baseline][3]
        new_msg.pose.orientation.x = baseline_matrix[cont_baseline][4]
        new_msg.pose.orientation.y = baseline_matrix[cont_baseline][5]
        new_msg.pose.orientation.z = baseline_matrix[cont_baseline][6]
        new_msg.pose.orientation.w = baseline_matrix[cont_baseline][7]
        
        cont_baseline += 1
        outbag.write(baseline_topic, new_msg, new_msg.header.stamp)
        outbag.write(topic, msg, t)
    elif ground_truth and topic==image_topic:
        if cont_gt < len(ground_truth_matrix):
            new_msg = Manhole()
            new_msg.id = int(ground_truth_matrix[cont_gt][2])
            new_msg.local_pose.x = ground_truth_matrix[cont_gt][3]
            new_msg.local_pose.y = ground_truth_matrix[cont_gt][4]
            new_msg.gps_position.latitude = graph_matrix[new_msg.id][0]
            new_msg.gps_position.longitude = graph_matrix[new_msg.id][1]
            outbag.write(ground_truth_topic,new_msg,t)
            cont_gt += 1
        outbag.write(topic,msg,t)
    else:
        outbag.write(topic,msg,t)
    print 'Completed: ', int((cont*100)/total),'%  Message: ', cont
    print "\033[F\033[F"
    cont += 1

print 'Added baseline. Number of baseline messages: {}'.format(cont_baseline)
print 'Added baseline. Number of old baseline messages: {}'.format(cont_alt_baseline)
if (ground_truth):
    print 'Added ground_truth. Number of ground_truth messages: {}'.format(cont_gt)
