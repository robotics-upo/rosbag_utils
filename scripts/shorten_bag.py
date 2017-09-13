#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <start time(s)> [duration (s)]'.format(sys.argv[0])
  sys.exit(-1)

cont = -1
end_t = -1

with rosbag.Bag(sys.argv[2], 'w') as outbag:
  for topic, msg, t in rosbag.Bag(sys.argv[1]).read_messages():
    if cont < 0:
      cont = 0 # Initialize the start and end times
      start_t = t + rospy.Duration(int(sys.argv[3]))
      if len(sys.argv) > 4:
        end_t = start_t + rospy.Duration(int(sys.argv[4]))
                        
    if len(sys.argv) > 4:
      if t > end_t:
        break
    
    if start_t < t:
      outbag.write(topic, msg, t)
      cont += 1
      
print 'Shortened the bag. Number of messages: {}'.format(cont)