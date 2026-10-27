from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    green_filter_node = Node(
        package='vision_control',
        executable='green_filter_node',
        name='green_filter',
        output='screen'
    )

    center_visual_servoing_node = Node(
        package='vision_control',
        executable='center_vs_node',
        name='center_vs',
        output='screen'
    )

    return LaunchDescription([
        green_filter_node,
        center_visual_servoing_node,
    ])