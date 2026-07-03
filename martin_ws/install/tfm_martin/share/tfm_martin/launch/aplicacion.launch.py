#!/usr/bin/env python3
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import PathJoinSubstitution
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():
    
    # ── 1. DRIVER OFICIAL DE INTEL REALSENSE ──────────────────────────────
    launch_realsense = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([
                FindPackageShare('realsense2_camera'), 
                'launch', 
                'rs_launch.py'
            ])
        ),
        launch_arguments={
            'align_depth.enable': 'true',        # Requerido para emparejar píxel a píxel depth y RGB
            'rgb_camera.profile': '640x480x30',   # Perfil de resolución de tu cámara
            'depth_module.profile': '848x480x30', # Perfil de resolución del sensor estéreo
        }.items(),
    )

    # ── 2. INCLUSIÓN DEL LAUNCHER DEL BRAZO uf850 ─────────────────────────
    # launch_uf850 = IncludeLaunchDescription(
    #     PythonLaunchDescriptionSource(
    #         PathJoinSubstitution([FindPackageShare('xarm_moveit_config'), 'launch', 'uf850_moveit_realmove.launch.py'])
    #     ),
    #     launch_arguments={'robot_ip': '192.168.1.234', 'hw_ns': 'ufactory'}.items(),
    # )

    # ── 3. INCLUSIÓN DEL LAUNCHER DEL xArm6 + MOTOR LINEAL ─────────────────
    launch_xarm6_lin_motor = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            PathJoinSubstitution([FindPackageShare('xarm_api'), 'launch', 'xarm6_driver.launch.py'])
        ),
        launch_arguments={'robot_ip': '192.168.1.211', 'hw_ns': 'xarm'}.items(),
    )

    # ── 4. TU NODO COORDINADOR CON REMAPPING NATIVO DE TÓPICOS ────────────
    nodo_coordinador = Node(
        package='tfm_martin',
        executable='coordinador_celda_colaborativa',
        name='Aplicacion_Coordinador_xArm6_MotorLineal_850_Collaborative',
        output='screen',
        # Interceptamos los tópicos oficiales y los traducimos a tus nombres personalizados
        remappings=[
            ('/camera/camera/color/image_raw', 'realsensed435/color_rgb_cam'),
            ('/camera/camera/depth/image_rect_raw', 'realsensed435/depth_cam'),
            ('/camera/camera/aligned_depth_to_color/camera_info', 'realsensed435/camera_info')
        ]
    )

    return LaunchDescription([
        launch_realsense,

        launch_xarm6_lin_motor,
        nodo_coordinador
    ])

        #launch_uf850,