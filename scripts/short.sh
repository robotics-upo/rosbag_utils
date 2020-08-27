for filename in *.bag
do
  rosbag filter $filename filtered_$filename "topic != '/cmd_vel' and topic != '/costmap_node/costmap' and topic != '/trajectory_marker' and topic != '/best_marker' and topic != '/operation_mode'"
done;
