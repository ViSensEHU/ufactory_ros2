ros2 launch camera_robot launch.py
ros2 run ros_gz_bridge parameter_bridge /world/default/model/my_robot/link/camera_link/sensor/camera_sensor/image@sensor_msgs/msg/Image[gz.msgs.Image
ros2 topic echo /world/default/model/my_robot/link/camera_link/sensor/camera_sensor/image

https://github.com/MOGI-ROS/Week-5-6-Gazebo-sensors?tab=readme-ov-file#rgbd-camera

--

root@f339d9dc7913:/home/javierac/camera_gz# git clone https://github.com/osrf/gazebo_models.git gazebo-11/models
#ENV GZ_SIM_RESOURCE_PATH=/usr/share/gazebo-11
#ENV GZ_SIM_MODEL_PATH=/usr/share/gazebo-11/models

export GZ_SIM_RESOURCE_PATH=/home/javierac/camera_gz/gazebo-11/models

root@f339d9dc7913:/home/javierac/camera_gz/mogi_trajectory_server# colcon build
Starting >>> mogi_trajectory_server
Finished <<< mogi_trajectory_server [1.30s]          

Summary: 1 package finished [1.43s]
root@f339d9dc7913:/home/javierac/camera_gz/mogi_trajectory_server# source install/setup.bash

root@f339d9dc7913:/home/javierac/camera_gz# colcon build --packages-skip gazebo_models

mkdir src
https://github.com/ros-tooling/topic_tools/tree/jazzy
git clone https://github.com/ros-tooling/topic_tools.git
cd ..
rosdep install --from-paths src -i -y
rm -rf build/ install/ log/
colcon build --packages-select topic_tools_interfaces topic_tools
colcon build --packages-skip topic_tools topic_tools_interfaces gazebo_models
source install/setup.bash

[ERROR] [launch]: Caught exception in launch (see debug for traceback): "package 'robot_localization' not found, searching: ['/home/javierac/camera_gz/install/topic_tools', '/home/javierac/camera_gz/install/topic_tools_interfaces', '/home/javierac/camera_gz/install/mogi_trajectory_server', '/home/javierac/camera_gz/install/bme_gazebo_sensors_py', '/home/javierac/camera_gz/install/bme_gazebo_sensors', '/home/xarm_ws/install/xarm_planner', '/home/xarm_ws/install/xarm_moveit_servo', '/home/xarm_ws/install/xarm_moveit_config', '/home/xarm_ws/install/xarm_gazebo', '/home/xarm_ws/install/xarm_controller', '/home/xarm_ws/install/xarm_api', '/home/xarm_ws/install/xarm_sdk', '/home/xarm_ws/install/xarm_msgs', '/home/xarm_ws/install/xarm_description', '/home/xarm_ws/install/mbot_demo', '/home/xarm_ws/install/uf_ros_lib', '/home/xarm_ws/install/realsense_gazebo_plugin', '/opt/ros/jazzy']"

sudo apt-get update
sudo apt-get install ros-jazzy-robot-localization

Para que la variable de entorno perdure: echo 'export GZ_SIM_RESOURCE_PATH=/home/javierac/camera_gz/gazebo-11/models' >> ~/.bashrc

EN RESUMEN:
ahora que está todo, nos ponemos en:
root@90fcba602f5a:/home/javierac/camera_gz#
Como está todo compilado: source install/setup.bash
Ejecutamos: ros2 launch bme_gazebo_sensors spawn_robot.launch.py
Para el teleop: ros2 run teleop_twist_keyboard teleop_twist_keyboard
