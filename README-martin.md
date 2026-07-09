```bash
ros2 run realsense2_camera realsense2_camera_node
```

https://github.com/realsenseai/realsense-ros#installation-on-ubuntu



```bash
cd /home/xarm_ws/
colcon build
source /home/xarm_ws/install/setup.bash

cd /home/$USER/martin_ws/
colcon build
source /home/$USER/martin_ws/install/setup.bash

root@078f02917823:/home/martinalangua/martin_ws# ros2 run realsense2_camera realsense2_camera_node

root@078f02917823:/home/martinalangua/martin_ws# ros2 run vision_grasping vision_node 

root@078f02917823:/home/xarm_ws# ros2 launch xarm_moveit_config xarm6_moveit_realmove.launch.py robot_ip:=192.168.1.211 auto_enable:=true

```