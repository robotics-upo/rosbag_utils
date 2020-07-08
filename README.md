# rosbag_utils
Some scripts for handling bags filtering stuff

## Processing MBZirc bags:

* M600 & M200 bags: just use:

'''
 add_tf_prefix.py <in_bag> <out_bag> /m600 

'''

* SIAR bags:

```

 change_t.py <in_bag> <out_bag> 

 change_global_tf <in_bag> <out_bag> world world_2d

```

* Then, merge the bags with merge_bag.py util

