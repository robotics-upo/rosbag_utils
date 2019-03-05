#!/bin/bash
if  [ $# -ne 2 ]; then
  echo "Use: $0 <input bag> <output_bag>"
  exit 1
fi
rosbag filter $1 $2 "topic != '/trajectory_marker' and topic != '/costmap_node/costmap' and topic != '/cmd_vel' and topic != '/best_marker'"