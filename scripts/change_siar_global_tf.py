#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 5):
  print 'Usage: {} <input bag> <output bag> <old_global_frame_id> <new_global_frame_id>'.format(sys.argv[0])
  sys.exit(-1)

if sys.argv[1] == sys.argv[2]:
  print 'Error: the input and output files have identical names'
  sys.exit(-2)

old_global_frame_id = sys.argv[3]
new_global_frame_id = sys.argv[4]

with rosbag.Bag(sys.argv[2], 'w') as outbag:
    with rosbag.Bag(sys.argv[1]) as bag:
        total = bag.get_message_count()
        print 'Total messages: ',total
        cont2 = 0
        changes = 0
        for topic, msg, t in bag.read_messages():
            if topic == '/tf' or topic == '/tf_static':
                for i in msg.transforms:
                    # print msg.transforms[0].header
                    # if old_global_frame_id in i.child_frame_id:
                    #     i.child_frame_id = new_global_frame_id
                    #     changes += 1
                    if old_global_frame_id in i.header.frame_id and 'siar' in i.child_frame_id:
                        i.header.frame_id = new_global_frame_id    
                        changes += 1
                        
            # if msg._has_header:
            #     if old_global_frame_id in msg.header.frame_id:
            #         msg.header.frame_id = new_global_frame_id
            #         changes += 1
                    
                
            print 'Completed: ', int((cont2*100)/total),'%  Changes: ', changes
            print "\033[F\033[F"
            
            cont2 += 1
            outbag.write(topic, msg, t)
 
print 'Added tf_prefix to all topics in the bag. Number of changes: {}'.format(changes)