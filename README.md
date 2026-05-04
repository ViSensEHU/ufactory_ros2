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

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.5, 0.0, 0.0, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, -0.7, -0.95, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

Detecta colisión con si mismo: ``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, 0.2, 0.1, 0.0, 0.0, 0.0], speed: 0.1, acc: 0.1, wait: true}"``

Códigos de error: https://github.com/xArm-Developer/xArm-Python-SDK/blob/master/doc/api/xarm_api_code.md

ros2 topic echo /xarm/robot_states

ros2 service type /xarm/motion_enable
