#!/usr/bin/python
import sys
import rosbag
import datetime
import rospy
from geometry_msgs import Transform

if (len(sys.argv) < 4):
  print 'Usage: {} <input bag> <output bag> <tf_change_file>'.format(sys.argv[0])
  print 'The tf_change_file should contain several lines. Each line: <original_tf_parent> <original_tf_child> <target_tf_parent> <targent_tf_child> <transform quaternion x y z w> <transform origin x y z>'
  print 'Example: electronics_center front_left_link front_link front_left_link 0 0 0 1 0 0 -0.2'
  sys.exit(-1)

with rosbag.Bag(sys.argv[2], 'w') as outbag:
  file = open(sys.argv[3],'r')
  cont = 0
  for line in file:
    split = line.split()
    if len(split)>=11:
      original_frame_id[cont] = split[0]
      original_child_id[cont] = split[1]
      target_frame_id[cont] = split[2]
      target_child_id[cont] = split[3]
      t = Transform()
      t.rotation.x = split[4]
      t.rotation.y = split[5]
      t.rotation.z = split[6]
      t.rotation.w = split[7]
      t.translation.x = split[8]
      t.translation.y = split[9]
      t.translation.z = split[10]
      
  
  #
  cont = 0
  for topic, msg, t in rosbag.Bag(sys.argv[1]).read_messages():
    
    for i in range(len(original_frame_id)):
      if topic=='tf':
	if (msg.header.frame_id == original_frame_id and msg.header.child_frame_id == original_child_id):
	  msg.header.frame_id = target_frame_id
	  msg.child_frame_id = target_child_id
	  msg.transform = transforms[i]
	  msg.rotation = target_rotation
      
    outbag.write(topic, msg, t)
    cont += 1
      
print 'Changed the transforms. Number of messages: {}'.format(cont)
