from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

import os

def generate_launch_description():
    # xArm driver
    # Equivale a: 
    """
    ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.238
    """
    xarm_api_dir = get_package_share_directory('xarm_api')
    xarm_driver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                xarm_api_dir,
                'launch',
                'xarm6_driver.launch.py'
            )
        ),
        launch_arguments={
            'robot_ip': '192.168.1.211'
        }.items()
    )

    # Nuestro nodo

    ejemplo_node = Node(
        package='ejemplo',
        executable='ejemplo',
        name='xarm_position_node',
        output='screen'
    )

    # Launch
    return LaunchDescription([
        xarm_driver,
        ejemplo_node,
    ])
