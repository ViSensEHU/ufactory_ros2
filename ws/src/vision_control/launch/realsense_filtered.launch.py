"""
realsense_filtered.launch.py
============================

Pipeline completo de filtros de profundidad recomendado por Intel para
RealSense D4xx, con un workaround automatico para el bug del parametro
`disparity_to_depth.enable` que no se puede pasar como launch arg en
algunas versiones del paquete realsense2_camera.

Pipeline aplicado (en orden, gestionado por el SDK):

    [depth raw]
        -> disparity_transform (depth -> disparity, ruido ~ cte)
        -> spatial_filter      (edge-preserving, alpha=0.6, delta=8)
        -> temporal_filter     (EMA temporal, alpha=0.5, delta=20)
        -> disparity_to_depth  (disparity -> depth)
        -> hole_filling_filter (left-fill de huecos residuales)
    [depth publicado en /xarm6/realsense/aligned_depth_to_color/image_raw]

Referencia: Intel RealSense D4xx whitepaper "Depth Post-Processing for
Intel RealSense D400 Depth Cameras" (Rev 1.0.2) - seccion B.

Como lanzarlo
-------------
    ros2 launch vision_control realsense_filtered.launch.py

Workaround del disparity_to_depth
---------------------------------
El rs_launch.py de algunas versiones no declara el argumento
`disparity_to_depth.enable` como DeclareLaunchArgument, asi que se
ignora al pasarlo como launch arg. Para evitar tener que hacer el
`ros2 param set` a mano, este launch lanza un ExecuteProcess retardado
que aplica el parametro 4 segundos despues del arranque del nodo.
"""

import os

from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    ExecuteProcess,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
    PackageShare,
)
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():

    # ============================================================
    # Argumentos del launch (con defaults recomendados por Intel)
    # ============================================================
    camera_namespace_arg = DeclareLaunchArgument(
        'camera_namespace', default_value='xarm6')
    camera_name_arg = DeclareLaunchArgument(
        'camera_name', default_value='realsense')

    # Streams
    align_depth_arg = DeclareLaunchArgument(
        'align_depth.enable', default_value='true')

    # Disparity transform (idida y vuelta)
    disparity_filter_arg = DeclareLaunchArgument(
        'disparity_filter.enable', default_value='true')

    # Spatial edge-preserving
    spatial_enable_arg = DeclareLaunchArgument(
        'spatial_filter.enable', default_value='true')
    spatial_magnitude_arg = DeclareLaunchArgument(
        'spatial_filter.filter_magnitude', default_value='2.0')
    spatial_alpha_arg = DeclareLaunchArgument(
        'spatial_filter.filter_smooth_alpha', default_value='0.6')
    spatial_delta_arg = DeclareLaunchArgument(
        'spatial_filter.filter_smooth_delta', default_value='8.0')
    spatial_holes_arg = DeclareLaunchArgument(
        'spatial_filter.holes_fill', default_value='1')

    # Temporal EMA
    temporal_enable_arg = DeclareLaunchArgument(
        'temporal_filter.enable', default_value='true')
    temporal_alpha_arg = DeclareLaunchArgument(
        'temporal_filter.filter_smooth_alpha', default_value='0.5')
    temporal_delta_arg = DeclareLaunchArgument(
        'temporal_filter.filter_smooth_delta', default_value='20.0')
    temporal_holes_arg = DeclareLaunchArgument(
        'temporal_filter.holes_fill', default_value='0')

    # Decimation (desactivado por defecto; activar si necesitas menos computo)
    decimation_enable_arg = DeclareLaunchArgument(
        'decimation_filter.enable', default_value='false')

    # Hole filling discreto (left-fill)
    hole_filling_enable_arg = DeclareLaunchArgument(
        'hole_filling_filter.enable', default_value='true')
    hole_filling_holes_arg = DeclareLaunchArgument(
        'hole_filling_filter.holes_fill', default_value='1')

    # ============================================================
    # IncludeLaunchDescription del rs_launch.py del paquete realsense2_camera
    # ============================================================
    realsense_share = get_package_share_directory('realsense2_camera')
    rs_launch_path = PathJoinSubstitution([
        realsense_share, 'launch', 'rs_launch.py'
    ])

    realsense_include = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(rs_launch_path),
        launch_arguments={
            'camera_namespace':                 LaunchConfiguration('camera_namespace'),
            'camera_name':                      LaunchConfiguration('camera_name'),
            'align_depth.enable':               LaunchConfiguration('align_depth.enable'),
            'disparity_filter.enable':          LaunchConfiguration('disparity_filter.enable'),
            'spatial_filter.enable':            LaunchConfiguration('spatial_filter.enable'),
            'spatial_filter.filter_magnitude':  LaunchConfiguration('spatial_filter.filter_magnitude'),
            'spatial_filter.filter_smooth_alpha': LaunchConfiguration('spatial_filter.filter_smooth_alpha'),
            'spatial_filter.filter_smooth_delta': LaunchConfiguration('spatial_filter.filter_smooth_delta'),
            'spatial_filter.holes_fill':        LaunchConfiguration('spatial_filter.holes_fill'),
            'temporal_filter.enable':           LaunchConfiguration('temporal_filter.enable'),
            'temporal_filter.filter_smooth_alpha': LaunchConfiguration('temporal_filter.filter_smooth_alpha'),
            'temporal_filter.filter_smooth_delta': LaunchConfiguration('temporal_filter.filter_smooth_delta'),
            'temporal_filter.holes_fill':       LaunchConfiguration('temporal_filter.holes_fill'),
            'decimation_filter.enable':         LaunchConfiguration('decimation_filter.enable'),
            'hole_filling_filter.enable':       LaunchConfiguration('hole_filling_filter.enable'),
            'hole_filling_filter.holes_fill':    LaunchConfiguration('hole_filling_filter.holes_fill'),
        }.items()
    )

    # ============================================================
    # WORKAROUND: aplicar disparity_to_depth.enable tras arrancar
    # ============================================================
    # Como rs_launch.py no declara este argumento, lo pasamos con
    # `ros2 param set` 4 segundos despues del arranque del nodo. El
    # nombre del nodo es <camera_namespace>/<camera_name> por defecto
    # en las versiones recientes del paquete.
    disparity_to_depth_fix = TimerAction(
        period=4.0,
        actions=[
            ExecuteProcess(
                cmd=[
                    'ros2', 'param', 'set',
                    '/xarm6/realsense',
                    'disparity_to_depth.enable',
                    'true'
                ],
                output='screen'
            )
        ]
    )

    # ============================================================
    # Nodos de la cadena pelota verde (opcional - comentar si ya los
    # lanzas desde green_follower.launch.py)
    # ============================================================
    green_filter_node = Node(
        package='vision_control',
        executable='green_filter_node',
        name='green_filter_node',
        output='screen'
    )

    center_visual_servoing_node = Node(
        package='vision_control',
        executable='center_visual_servoing',
        name='center_visual_servoing',
        output='screen'
    )

    tracking_node = Node(
        package='vision_control',
        executable='tracking_node',
        name='tracking_node',
        output='screen'
    )

    grasping_node = Node(
        package='vision_control',
        executable='grasping_node',
        name='grasping_node',
        parameters=[{
            'ball_radius_mm':        10.0,
            'camera_to_gripper_mm':   120.0,
            'gripper_close_drop_mm':  10.7,
            'depth_bias_mm':          0.0,
            'kf_q':                   5.0,
            'kf_R0':                  8.0,
            'kf_z_ref':               400.0,
        }],
        output='screen'
    )

    main_fsm_node = Node(
        package='vision_control',
        executable='main_fsm',
        name='main_fsm',
        output='screen'
    )

    return LaunchDescription([
        # Argumentos
        camera_namespace_arg,
        camera_name_arg,
        align_depth_arg,
        disparity_filter_arg,
        spatial_enable_arg,
        spatial_magnitude_arg,
        spatial_alpha_arg,
        spatial_delta_arg,
        spatial_holes_arg,
        temporal_enable_arg,
        temporal_alpha_arg,
        temporal_delta_arg,
        temporal_holes_arg,
        decimation_enable_arg,
        hole_filling_enable_arg,
        hole_filling_holes_arg,
        # Pipeline RealSense + workaround
        realsense_include,
        disparity_to_depth_fix
        # Nodos de la cadena
        #green_filter_node,
        #center_visual_servoing_node,
        #tracking_node,
        #grasping_node,
        #main_fsm_node,
    ])
