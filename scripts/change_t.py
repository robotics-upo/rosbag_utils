#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <time_offset>'.format(sys.argv[0])
  sys.exit(-1)

if sys.argv[1] == sys.argv[2]:
  print 'Error: the input and output files have identical names'
  sys.exit(-2)

time_offset = rospy.Duration(float(sys.argv[3]))

with rosbag.Bag(sys.argv[2], 'w') as outbag:
    with rosbag.Bag(sys.argv[1]) as bag:
        total = bag.get_message_count()
        print 'Total messages: ',total
        cont2 = 0
        changes = 0
        for topic, msg, t in bag.read_messages():
            print 'Completed: ', int((cont2*100)/total),'%  Message: ', cont2
            print "\033[F\033[F"
               
            # if "siar" in topic:
            t = t + time_offset 
            if msg._has_header:
              msg.header.stamp = msg.header.stamp + time_offset
              changes += 1
            if "tf" in topic:
              
              for i in msg.transforms:
              
                # if "siar" in i.header.frame_id or "siar" in i.child_frame_id: 
                  # changes += 1
                  i.header.stamp = i.header.stamp + time_offset
              
            cont2 += 1
            outbag.write(topic, msg, t)
            
  
print 'Corrected time in the topics and tfs. Number of changes: {}'.format(changes)