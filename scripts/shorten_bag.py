#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <start time(s)> [duration (s)]'.format(sys.argv[0])
  sys.exit(-1)

if sys.argv[1] == sys.argv[2]:
  print 'Error: the input and output files have identical names'
  sys.exit(-2)

cont = -1
end_t = -1


with rosbag.Bag(sys.argv[2], 'w') as outbag:
  bag = rosbag.Bag(sys.argv[1])
  
  total = bag.get_message_count()
  print 'Total messages: ',total
  cont2 = 0
  for topic, msg, t in bag.read_messages():
    if cont < 0:
      cont = 0 # Initialize the start and end times
      
      start_t = t + rospy.Duration(int(sys.argv[3]))
      if len(sys.argv) > 4:
        end_t = start_t + rospy.Duration(int(sys.argv[4]))
                        
    if len(sys.argv) > 4:
      if t > end_t:
        break
    
    print 'Completed: ', int((cont2*100)/total),'%  Message: ', cont2
    print "\033[F\033[F"
    
    cont2 += 1
    
    if start_t < t:
      outbag.write(topic, msg, t)
      cont += 1
      
print 'Shortened the bag. Number of messages: {}'.format(cont)