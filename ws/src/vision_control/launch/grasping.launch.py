from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    tracking_node = Node(
        package='vision_control',
        executable='tracking_node',
        name='tracking',
        output='screen'
    )

    grasping_node = Node(
        package='vision_control',
        executable='grasping_node',
        name='grasping',
        output='screen'
    )

    main_node = Node(
        package='vision_control',
        executable='main_fsm_node',
        name='main_fsm',
        output='screen'
    )

    return LaunchDescription([
        tracking_node,
        grasping_node,
        main_node,
    ])