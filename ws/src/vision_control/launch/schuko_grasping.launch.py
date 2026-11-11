from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    yolo_node = Node(
            package='vision_control',
            executable='schuko_detection_node',
            name='schuko_yolo',
            output='screen'
    )
    
    tracking_node = Node(
        package='vision_control',
        executable='tracking_schuko_node',
        name='tracking_schuko',
        output='screen'
    )

    grasping_node = Node(
            package='vision_control',
            executable='grasping_schuko_node',
            name='grasping_schuko',
            output='screen'
    )

    center_visual_servoing_node = Node(
            package='vision_control',
            executable='center_vs_schuko_node',
            name='center_vs',
            output='screen'
    )

    main_node = Node(
            package='vision_control',
            executable='main_schuko_fsm_node',
            name='main_schuko_fsm',
            output='screen'
    )

    return LaunchDescription([
        yolo_node,
        tracking_node,
        grasping_node,
        center_visual_servoing_node,
        main_node
    ])