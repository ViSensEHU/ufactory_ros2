import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/isaac_sim/ros2_ws/install/xarm6_policy_infer'
