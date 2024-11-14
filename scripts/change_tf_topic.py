#!/usr/bin/python3
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 5):
  print('Usage: {} <input bag> <output bag> <topic> <new_frame_id>'.format(sys.argv[0]))
  sys.exit(-1)

with rosbag.Bag(sys.argv[2], 'w') as outbag:
  cont = 0
  for topic, msg, t in rosbag.Bag(sys.argv[1]).read_messages():
    
    if topic==sys.argv[3]:
      msg.header.frame_id = sys.argv[4]
    outbag.write(topic, msg, t)
    cont += 1
      
print('Changed the transforms. Number of messages: {}'.format(cont))
