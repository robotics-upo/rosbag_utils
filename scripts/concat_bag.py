#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 5):
  print 'Usage: {} <input bag 1 > <input bag 2> <output bag> <start time bag 1(s)> [duration bag 2(s)]'.format(sys.argv[0])
  sys.exit(-1)

cont = -1
end_t = -1


with rosbag.Bag(sys.argv[3], 'w') as outbag:
  print 'Openning bag 1. File: ', sys.argv[1]
  bag_1 = rosbag.Bag(sys.argv[1])
  
  
  total = bag_1.get_message_count()
  print 'Processing bag 1. Total messages: ',total
  cont2 = 0
  for topic, msg, t in bag_1.read_messages():
    if cont < 0:
      cont = 0 # Initialize the start and end times
      
      start_t = t + rospy.Duration(int(sys.argv[4]))
    if start_t < t:
      outbag.write(topic, msg, t)
      cont += 1    
    cont2 += 1
    print 'Completed: ', int((cont2*100)/total),'%  Message: ', cont2
    print "\033[F\033[F"
      
  # Bag 2 Processing
  print 'Openning bag 2. File: ', sys.argv[2]
  bag_2 = rosbag.Bag(sys.argv[2])
  total = bag_2.get_message_count()
  print 'Processing bag 2. Total messages: ',total
  cont2 = 0
  for topic,msg, t in bag_2.read_messages():
    if cont2 == 0:
      start_t = t
      if len(sys.argv) > 5:
        end_t = start_t + rospy.Duration(int(sys.argv[5]))
    if len(sys.argv) > 5:
      if t > end_t:
        break
    print 'Completed: ', int((cont2*100)/total),'%  Message: ', cont2
    print "\033[F\033[F"
    outbag.write(topic, msg, t)
    cont += 1
    cont2 += 1
      
print 'Shortened the bag. Number of messages: {}'.format(cont)