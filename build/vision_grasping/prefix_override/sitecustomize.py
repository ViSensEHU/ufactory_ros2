import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/home/martinalangua/Desktop/ufactory_ros2/install/vision_grasping'
