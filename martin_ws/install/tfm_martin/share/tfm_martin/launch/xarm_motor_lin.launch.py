#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    # 1. Levantamos EXCLUSIVAMENTE el driver de la controladora xArm
    launch_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('xarm_api'), 
                'launch', 
                'xarm6_driver.launch.py'
            ])
        ),
        launch_arguments={
            'robot_ip': '192.168.1.211',
            'hw_ns': 'xarm',
        }.items(),
    )

    # 2. Tu nodo de pruebas
    nodo_prueba = Node(
        package='tfm_martin',
        executable='run',
        name='xArm_motor_lineal_test_node',
        output='screen'
    )

    return LaunchDescription([
        launch_driver,
        nodo_prueba
    ])