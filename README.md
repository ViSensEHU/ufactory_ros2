# FALTA AÑADIR CÓMO HE ARREGLADO LO DE NVIDIA
en el host es necesario: sudo prime-select nvidia
y al ejecutar "glxinfo | grep "OpenGL renderer" que aparezca NVIDIA

--

# Visualizar en RVIZ2 y mover las joints
En una terminal: 
```bash
ros2 launch xarm_description xarm6_rviz_display.launch.py add_gripper:=true
```

En otra terminal:
```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```

# xArm moveit config
ros2 launch xarm_moveit_config xarm6_moveit_fake.launch.py [add_gripper:=true]


# xArm planner
En una terminal:
```bash
ros2 launch xarm_planner xarm6_planner_fake.launch.py [add_gripper:=true]
```

En otra terminal:
```bash
ros2 launch xarm_planner test_xarm_planner_api_joint.launch.py dof:=6 robot_type:=xarm
```
o 
```bash
ros2 launch xarm_planner test_xarm_planner_api_pose.launch.py dof:=6 robot_type:=xarm
```