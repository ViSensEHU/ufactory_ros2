# Generar .urdf del .xacro de xArm6 de UFactory (pendiente de documentar con más detalle)
Dentro del contenedor de Docker de ROS2:
1. ```cd /home/isaac_sim/projects/ufactory_ros2/xarm_ros2```
2. ```colcon build --packages-select xarm_description```
3. ```source install/setup.bash```
4. ```cd /home/isaac_sim/projects/ufactory_ros2/xarm_ros2/xarm_description/urdf```
5. ```xacro xarm_device.urdf.xacro   dof:=6   robot_type:=xarm   hw_ns:=xarm   limited:=true   velocity_control:=false   effort_control:=false   add_gripper:=false   -o xarm6.urdf```
6. ```xacro xarm_device.urdf.xacro   dof:=6   robot_type:=xarm   hw_ns:=xarm   limited:=true   velocity_control:=false   effort_control:=false   add_gripper:=true   -o xarm6_with_gripper.urdf```
7. ```xacro xarm_device.urdf.xacro robot_type:=uf850 dof:=6 hw_ns:=xarm limited:=true velocity_control:=false effort_control:=false add_gripper:=false -o uf850.urdf```
8. ```xacro xarm_device.urdf.xacro robot_type:=uf850 dof:=6 hw_ns:=xarm limited:=true velocity_control:=false effort_control:=false add_gripper:=true -o uf850_with_gripper.urdf```


# Para ejecutar entrenamiento UFXarm6:
Copiar la carpeta ``/workspace/isaaclab/_isaac_sim/projects/ufactory_ros2/isaac-sim/scripts/train/base/uf_xarm6`` en ``/workspace/isaaclab/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/reach/config``.

Ejecutar ``./isaaclab.sh -p scripts/reinforcement_learning/skrl/train.py --task Isaac-Reach-XArm6-v0 --num_envs 600``, para ver los logs ``./isaaclab.sh -p -m tensorboard.main --logdir logs/skrl/reach_franka/``, para play ``./isaaclab.sh -p scripts/reinforcement_learning/skrl/play.py --task Isaac-Reach-XArm6-v0 --num_envs 32``

# Para controlar el robot real desde MoveIt
``ros2 launch xarm_moveit_config xarm6_moveit_realmove.launch.py robot_ip:=192.168.1.238 auto_enable:=true``

Para lanzar el controller sin moveit2: ``ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.238``

```
cd ~/dev_ws/
# launch xarm_driver_node:
ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.117

# enable all joints:
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetInt16ById "{id: 8, data: 1}"

# disable
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetInt16ById "{id: 8, data: 0}"

# set proper mode (0) and state (0)
ros2 service call /xarm/set_mode xarm_msgs/srv/SetInt16 "{data: 0}"
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# Cartesian linear motion: (unit: mm, rad)
ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian "{pose: [300, 0, 250, 3.14, 0, 0], speed: 50, acc: 500, mvtime: 0}"   

# joint motion for xArm6: (unit: rad)
ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [-0.58, 0, 0, 0, 0, 0], speed: 0.35, acc: 10, mvtime: 0}"
```

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.5, 0.0, 0.0, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, -0.7, -0.95, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

Detecta colisión con si mismo: ``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, 0.2, 0.1, 0.0, 0.0, 0.0], speed: 0.1, acc: 0.1, wait: true}"``

Códigos de error: https://github.com/xArm-Developer/xArm-Python-SDK/blob/master/doc/api/xarm_api_code.md

ros2 topic echo /xarm/robot_states

ros2 service type /xarm/motion_enable

# Nodo inferencia ROS2
``ros2 launch xarm_moveit_config xarm6_moveit_fake.launch.py [add_gripper:=true]``
``ros2 run xarm6_policy_infer infer``

Se mueve en RViz con:
```bash
ros2 topic pub /xarm6_traj_controller/joint_trajectory trajectory_msgs/JointTrajectory "
joint_names:
- 'joint1'
- 'joint2'
- 'joint3'
- 'joint4'
- 'joint5'
- 'joint6'
points:
- positions: [0.0, -0.15, -0.15, 0.0, 0.0, 0.0]
  time_from_start:
    sec: 1
    nanosec: 0
"
```

```bash
ros2 topic pub /goal_pose geometry_msgs/PoseStamped "
header:
  frame_id: 'base_link'
pose:
  position:
    x: 0.4
    y: 0.0
    z: 0.3
  orientation:
    x: 0.0
    y: 0.0
    z: 0.0
    w: 1.0
"
```