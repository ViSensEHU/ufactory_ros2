from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    xarm_visual_servo_controller_lifecycle_node = Node(
        package='vision_control',
        executable='xarm_visual_servo_controller_lifecycle',
        name='xarm_visual_servo_controller_lifecycle',
        output='screen'
    )

    main_node = Node(
        package='vision_control',
        executable='main',
        name='main',
        output='screen'
    )

    return LaunchDescription([
        xarm_visual_servo_controller_lifecycle_node,
        main_node,
    ])