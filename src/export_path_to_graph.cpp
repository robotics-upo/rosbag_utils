#include <rosbag/bag.h>
#include <rosbag/view.h>
#include <nav_msgs/Path.h>
#include "ros/ros.h"
#include <limits>
#include <string>
#include <vector>
#include <fstream>
#include <ros/serialization.h>
#include <sys/stat.h>


using namespace std;
namespace ser = ros::serialization;

int main(int argc, char **argv) 
{
  rosbag::Bag inbag;
  rosbag::Bag outbag;
  if (argc != 4) {
    cerr << "Usage: " << argv[0] << " <bag file> <out_bag> <path_file> \n";
    return -1;
  }

    struct stat st;
    stat(argv[2],&st);
    auto size = st.st_size;
  
  std::string gt_topic = "/ground_truth";

  try {
    inbag.open(argv[1]);
    outbag.open(argv[2], rosbag::bagmode::Write);
    rosbag::View view(inbag);
    bool initialized = false;
    bool _positive = false;
    bool ignoring = true;

    nav_msgs::Path path;

    const uint32_t serial_size = size;
    boost::shared_array<uint8_t> buffer(new uint8_t[serial_size]);

    ser::IStream stream(buffer.get(), serial_size);
    ser::deserialize(stream, path);


    ROS_INFO("Path loaded. Path length: %ld", path.poses.size());

    std::vector<geometry_msgs::PoseStamped>::iterator it = path.poses.begin();

    for (rosbag::MessageInstance &m:view)
    {
      if (it != path.poses.end() && m.getTime() > it->header.stamp) {
        outbag.write(gt_topic, it->header.stamp, *it);
        it++;
      }
      outbag.write(m.getTopic(), m.getTime(), m);
    }

    inbag.close();
    outbag.close();
  } catch (exception &e) {
    cerr << "Exception while manipulating the bag  " << argv[1] << endl;
    cerr << "Content " << e.what() << endl;
    return -2;
  }

  
  return 0;
}

