#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <tf_prefix> [<global_frame_id>]'.format(sys.argv[0])
  sys.exit(-1)

if sys.argv[1] == sys.argv[2]:
  print 'Error: the input and output files have identical names'
  sys.exit(-2)

cont = 0
end_t = -1

prefix = sys.argv[3]
if prefix[len(prefix)-1] != '/':
    tf_prefix = prefix + '/'
else:
    tf_prefix = prefix
    prefix = prefix[0:len(prefix)-1]
    
print 'Adding prefix: ' + prefix + "\tTf prefix: " + tf_prefix

global_frame_id = 'world'
if len(sys.argv) > 4:
     global_frame_id = sys.argv[4]

ignored = 0
with rosbag.Bag(sys.argv[2], 'w') as outbag:
    with rosbag.Bag(sys.argv[1]) as bag:
        total = bag.get_message_count()
        print 'Total messages: ',total
        cont2 = 0
        for topic, msg, t in bag.read_messages():
            if topic == '/tf' or topic == '/tf_static':
                for i in msg.transforms:
                    # print msg.transforms[0].header
                    if not global_frame_id in i.child_frame_id:
                        i.child_frame_id = tf_prefix + i.child_frame_id
                        cont += 1
                    if not global_frame_id in i.header.frame_id:
                        i.header.frame_id = tf_prefix + i.header.frame_id    
                        cont += 1
                    
            else:
                topic = '/' + prefix + topic
                
            if msg._has_header:
                if not(global_frame_id in msg.header.frame_id):
                    msg.header.frame_id = tf_prefix + msg.header.frame_id
                    cont += 1
                    
                
            print 'Completed: ', int((cont2*100)/total),'%  Message: ', cont2
            print "\033[F\033[F"
            
            cont2 += 1
            outbag.write(topic, msg, t)

      
print 'Added tf_prefix to all topics in the bag. Changes: {}'.format(cont)