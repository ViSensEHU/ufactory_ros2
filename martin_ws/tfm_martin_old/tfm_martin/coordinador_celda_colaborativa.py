#!/usr/bin/env python3
"""
coordinador_celda_colaborativa.py
================================
Orquestador de Celda Colaborativa basado en Tópicos nativos de ROS 2.
Elimina hilos manuales de Python y procesa la visión a través de callbacks del Executor.
Manteniendo la estructura original de argumentos para MoveCartesian.Request.
"""

import rclpy
import time
import math
import numpy as np
from rclpy.node import Node
from rclpy.executors import MultiThreadedExecutor
from rclpy.callback_groups import ReentrantCallbackGroup

# Interfaces estándar de ROS 2 para tratamiento de imágenes
from sensor_msgs.msg import Image, CameraInfo
from cv_bridge import CvBridge

from xarm_msgs.srv import (
    SetInt16,
    SetInt16ById,
    LinearMotorSetPos,
    LinearMotorBackOrigin,
    MoveCartesian,
    MoveJoint,
    GripperMove,
)

from tfm_martin.cv_grasp_detector import CVGraspDetector
from tfm_martin.helpers.matrix_funcs import euler2mat, convert_pose

class MinPos():
    def __init__(self, inputs, time_steps):
        self.buffer = np.zeros((time_steps, inputs))
        self.steps = time_steps
        self.curr = 0
        self.been_reset = True
        self.prev_pos = [0.0, 0.0, 0.0, 0.0]

    def update(self, v):
        if self.steps == 1: return v
        self.buffer[self.curr, :] = v
        self.curr += 1
        if self.been_reset:
            self.been_reset = False
            while self.curr != 0: self.update(v)
        if self.curr >= self.steps: self.curr = 0
        min_dis = 9999.0
        min_inx = 0
        for i in range(self.steps):
            dis = (pow(self.buffer[i][0] - self.prev_pos[0], 2) + 
                   pow(self.buffer[i][1] - self.prev_pos[1], 2) + 
                   pow(self.buffer[i][2] - self.prev_pos[2], 2))
            if dis < min_dis:
                min_dis = dis; min_inx = i
        self.prev_pos = list(self.buffer[min_inx, :])
        return self.prev_pos

    def reset(self):
        self.buffer *= 0; self.curr = 0; self.been_reset = True


class CoordinadorCeldaNode(Node):

    def __init__(self):
        super().__init__('coordinador_celda_node')
        self.get_logger().info('Inicializando Celda Colaborativa por Tópicos de ROS 2...')

        # ReentrantCallbackGroup permite que las suscripciones de imágenes corran en paralelo con los servicios
        self.callback_group = ReentrantCallbackGroup()
        self.bridge = CvBridge()

        # ── 1. PARÁMETROS GEOMÉTRICOS ORIGINALES ─────────────────────────────
        self.xarm_initpos_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Radianes
        self.xarm_detect_xyz     = [220.5, 0.0, 575.0]             # mm
        self.xarm_release_xyz    = [0.0, 360.5, 488.0]             # mm
        self.linear_pos_scan     = 50                              # mm
        self.linear_pos_inter    = 700                             # mm

        self.u850_initpos_angles = [0.0, 0.0, math.radians(-45.0), 0.0, math.radians(-45.0), 0.0]
        self.u850_grasp_xyz      = [575.1, 23.2, 590.0]
        self.u850_grasp_rpy      = [math.radians(90), 0.0, math.radians(90)]
        
        self.deposit_slots = [
            {'xyz': [57.8, -644.6, 650.0],  'rpy': [180.0, 0.0, 0.0], 'occupied': 0, 'row': 1, 'column': 1},
            {'xyz': [215.7, -644.6, 650.0], 'rpy': [180.0, 0.0, 0.0], 'occupied': 0, 'row': 1, 'column': 2},
            {'xyz': [56.9, -484.9, 361.0],  'rpy': [-152.0, -87.8, -116.3], 'occupied': 0, 'row': 2, 'column': 1},
            {'xyz': [207.3, -484.9, 361.0], 'rpy': [-152.0, -87.8, -116.3], 'occupied': 0, 'row': 2, 'column': 2},
        ]
        self.container_xyz = [300.0, 300.0, 370.0]

        # Estructura de calibración estática Ojo-Mano [X_mm, Y_mm, Z_mm, Roll, Pitch, Yaw]
        self.euler_eef_to_color_opt = [67.052, -31.138, 21.611, -0.004202, -0.008485, 1.589877]
        self.euler_eef_to_color_opt2 = self.euler_eef_to_color_opt.copy()
        self.euler_eef_to_color_opt2[0] = 0.0
        self.euler_eef_to_color_opt2[1] = 0.0
        self.euler_color_to_depth_opt = [0.015, 0.0, 0.0, 0.0, 0.0, 0.0]
        
        self.grasping_range = [-180.0, 650.0, -480.0, 480.0]
        self.lift_height    = self.xarm_detect_xyz[2]
        self.gripper_z_mm   = 150.0
        self.grasping_min_z = 0.0
        self.min_result_z   = 200.0 / 1000.0

        # ── 2. VARIABLES DE ENTORNO CONCURRENTE (MÁQUINA DE ESTADOS) ─────────
        self.CURR_POS         = [220.5, 0.0, 650.0, 180.0, 0.0, 0.0]
        self.GOAL_POS         = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.GRASP_STATUS     = 0
        
        self.ready_check      = False
        self.ready_grasp      = False
        self.alive            = True
        self.last_grasp_time  = time.monotonic()

        self.pose_averager    = MinPos(4, 3)
        self.pose_averager2   = MinPos(4, 3)

        # ── 3. CLIENTES ROS 2 (Callback group concurrente asignado) ──────────
        self.cli_lin_enable     = self.create_client(SetInt16, '/xarm/set_linear_motor_enable', callback_group=self.callback_group)
        self.cli_lin_speed      = self.create_client(SetInt16, '/xarm/set_linear_motor_speed', callback_group=self.callback_group)
        self.cli_lin_origin     = self.create_client(LinearMotorBackOrigin, '/xarm/set_linear_motor_back_origin', callback_group=self.callback_group)
        self.cli_lin_pos        = self.create_client(LinearMotorSetPos, '/xarm/set_linear_motor_pos', callback_group=self.callback_group)
        self.cli_xarm_mode      = self.create_client(SetInt16, '/xarm/set_mode', callback_group=self.callback_group)
        self.cli_xarm_state     = self.create_client(SetInt16, '/xarm/set_state', callback_group=self.callback_group)
        self.cli_xarm_pos       = self.create_client(MoveCartesian, '/xarm/set_position', callback_group=self.callback_group)
        self.cli_xarm_joints    = self.create_client(MoveJoint, '/xarm/set_servo_angle', callback_group=self.callback_group)
        self.cli_xarm_enable    = self.create_client(SetInt16ById, '/xarm/motion_enable', callback_group=self.callback_group)
        self.cli_xarm_grip_en   = self.create_client(SetInt16, '/xarm/set_gripper_enable', callback_group=self.callback_group)
        self.cli_xarm_grip_mode = self.create_client(SetInt16, '/xarm/set_gripper_mode', callback_group=self.callback_group)
        self.cli_xarm_grip_pos  = self.create_client(GripperMove, '/xarm/set_gripper_position', callback_group=self.callback_group)

        self.cli_850_mode       = self.create_client(SetInt16, '/ufactory/set_mode', callback_group=self.callback_group)
        self.cli_850_state      = self.create_client(SetInt16, '/ufactory/set_state', callback_group=self.callback_group)
        self.cli_850_pos        = self.create_client(MoveCartesian, '/ufactory/set_position', callback_group=self.callback_group)
        self.cli_850_joints     = self.create_client(MoveJoint, '/ufactory/set_servo_angle', callback_group=self.callback_group)
        self.cli_850_enable     = self.create_client(SetInt16ById, '/ufactory/motion_enable', callback_group=self.callback_group)

        self._wait_all_services()

        # ── 4. SUSCRIPCIONES ASÍNCRONAS DE LA CÁMARA ─────────────────────────
        self.latest_color_img = None
        self.camera_k = None
        self.detector = None

        self.sub_info = self.create_subscription(
            CameraInfo, 'realsensed435/camera_info', self.camera_info_callback, 10, callback_group=self.callback_group
        )
        self.sub_color = self.create_subscription(
            Image, 'realsensed435/color_rgb_cam', self.color_callback, 10, callback_group=self.callback_group
        )
        self.sub_depth = self.create_subscription(
            Image, 'realsensed435/depth_cam', self.depth_callback, 10, callback_group=self.callback_group
        )

        # Timer cíclico para la máquina de estados reactiva (100Hz)
        self.timer_check = self.create_timer(0.01, self.check_callback, callback_group=self.callback_group)

        # Timer One-Shot nativo para arrancar la inicialización de forma asíncrona
        self.timer_arranque = self.create_timer(0.1, self._timer_arranque_callback, callback_group=self.callback_group)

    def _timer_arranque_callback(self):
        self.timer_arranque.cancel()
        self.run_initialization()

    def _wait_all_services(self):
        services = [
            (self.cli_lin_enable, '/xarm/set_linear_motor_enable'),
            (self.cli_lin_speed,  '/xarm/set_linear_motor_speed'),
            (self.cli_lin_origin, '/xarm/set_linear_motor_back_origin'),
            (self.cli_lin_pos,    '/xarm/set_linear_motor_pos'),
            (self.cli_xarm_mode,     '/xarm/set_mode'),
            (self.cli_xarm_state,    '/xarm/set_state'),
            (self.cli_xarm_pos,      '/xarm/set_position'),
            (self.cli_xarm_joints,   '/xarm/set_servo_angle'),
            (self.cli_xarm_enable, '/xarm/motion_enable'),
            (self.cli_xarm_grip_en,   '/xarm/set_gripper_enable'),   
            (self.cli_xarm_grip_mode, '/xarm/set_gripper_mode'),   
            (self.cli_xarm_grip_pos,  '/xarm/set_gripper_position'), 
            # (self.cli_850_mode,    '/ufactory/set_mode'),
            # (self.cli_850_state,   '/ufactory/set_state'),
            # (self.cli_850_pos,     '/ufactory/set_position'),
            # (self.cli_850_joints,  '/ufactory/set_servo_angle'),
            # (self.cli_850_enable,  '/ufactory/motion_enable'),
        ]
        for client, name in services:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Esperando servicio crítico {name}...')

    def camera_info_callback(self, msg):
        if self.camera_k is not None: return
        self.camera_k = np.array([
            [msg.k[0], 0.0,      msg.k[2]],
            [0.0,      msg.k[4], msg.k[5]],
            [0.0,      0.0,      1.0     ]
        ])
        detector_config = {'OPEN_LOOP_HEIGHT': 340, 'GGCNN_IN_THREAD': False, 'DEPTH_CAM_K': self.camera_k}
        self.detector = CVGraspDetector(detector_config, None, None)
        self.get_logger().info('[VISIÓN] Matriz intrínseca capturada desde el tópico. Detector de momentos online.')

    def color_callback(self, msg):
        try:
            self.latest_color_img = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')
        except Exception as e:
            self.get_logger().error(f'Error decodificando flujo RGB: {e}')

    def depth_callback(self, msg):
        if not self.ready_check or not self.ready_grasp or self.detector is None or self.latest_color_img is None:
            return

        try:
            depth_image_raw = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
            depth_image = depth_image_raw.astype(np.float32) * 0.001
            depth_image[depth_image == 0] = np.nan

            self.detector._color_img = self.latest_color_img
            robot_z_m = self.CURR_POS[2] / 1000.0
            _, result = self.detector.get_grasp_img(depth_image, self.camera_k, robot_z_m)

            if result and result[2] > self.min_result_z:
                euler_base_to_eef = [self.CURR_POS[0]*0.001, self.CURR_POS[1]*0.001, self.CURR_POS[2]*0.001,
                                     math.radians(self.CURR_POS[3]), math.radians(self.CURR_POS[4]), math.radians(self.CURR_POS[5])]
                
                gp = [result[0], result[1], result[2], 0.0, 0.0, -1.0 * result[3]]

                mat_depthOpt_in_base = euler2mat(euler_base_to_eef) * euler2mat(self.euler_eef_to_color_opt) * euler2mat(self.euler_color_to_depth_opt)
                mat_depthOpt_in_base2 = euler2mat(euler_base_to_eef) * euler2mat(self.euler_eef_to_color_opt2) * euler2mat(self.euler_color_to_depth_opt)
                
                gp_base = convert_pose(gp, mat_depthOpt_in_base)
                gp_base2 = convert_pose(gp, mat_depthOpt_in_base2)

                for g in [gp_base, gp_base2]:
                    if g[5] < -np.pi: g[5] += np.pi
                    elif g[5] > 0: g[5] -= np.pi

                av = self.pose_averager.update(np.array([gp_base[0], gp_base[1], gp_base[2], gp_base[5]]))
                av2 = self.pose_averager2.update(np.array([gp_base2[0], gp_base2[1], gp_base2[2], gp_base2[5]]))
                
                if self.GRASP_STATUS == 0:
                    av = av2
                
                ang = av[3] - np.pi / 2
                GOAL_POS = [av[0] * 1000.0, av[1] * 1000.0, av[2] * 1000.0 + self.gripper_z_mm, 180.0, 0.0, math.degrees(ang + np.pi)]
                GOAL_POS[2] = max(GOAL_POS[2], self.grasping_min_z)

                if (GOAL_POS[0] < self.grasping_range[0] or GOAL_POS[0] > self.grasping_range[1] or 
                    GOAL_POS[1] < self.grasping_range[2] or GOAL_POS[1] > self.grasping_range[3]):
                    return

                self.last_grasp_time = time.monotonic()
                self.GOAL_POS = GOAL_POS

                # MANTENIENDO TU ESTRUCTURA ORIGINAL DE ARGUMENTOS DIRECTOS REQ
                if self.GRASP_STATUS == 0:
                    z_segura = self.xarm_detect_xyz[2]
                    req = MoveCartesian.Request(x=self.GOAL_POS[0], y=self.GOAL_POS[1], z=z_segura,
                                                roll=self.GOAL_POS[3], pitch=self.GOAL_POS[4], yaw=self.GOAL_POS[5],
                                                speed=100.0, acc=1000.0, wait=False)
                    self.cli_xarm_pos.call_async(req)

                elif self.GRASP_STATUS == 1:
                    z_segura = self.xarm_detect_xyz[2]
                    req = MoveCartesian.Request(x=self.GOAL_POS[0], y=self.GOAL_POS[1], z=z_segura,
                                                roll=self.GOAL_POS[3], pitch=self.GOAL_POS[4], yaw=self.GOAL_POS[5],
                                                speed=80.0, acc=1000.0, wait=False)
                    self.cli_xarm_pos.call_async(req)
                    self.GRASP_STATUS = 2

        except Exception as e:
            self.get_logger().error(f'Error en cálculo reactivo de visión: {e}')

    def call_services_parallel(self, calls: list[tuple]) -> list:
        futures = []
        for client, request, label in calls:
            futures.append((client.call_async(request), label))
        results = []
        for future, label in futures:
            while rclpy.ok() and not future.done():
                time.sleep(0.002)
            results.append(future.result() if rclpy.ok() else None)
        return results

    def get_next_free_slot(self):
        for slot in self.deposit_slots:
            if slot['occupied'] == 0: return slot['xyz'], slot
        return self.container_xyz, None

    def run_initialization(self):
        self.get_logger().info('[INIT] Referenciando potencias y homes cartesianos...')
        
        self.call_services_parallel([
            (self.cli_lin_enable, SetInt16.Request(data=1), 'Habilitar Motor Lineal'),
            (self.cli_xarm_enable, SetInt16ById.Request(id=8, data=1), 'Habilitar xArm6'),
            #(self.cli_850_enable, SetInt16ById.Request(id=8, data=1), 'Habilitar uFactory 850'),
            (self.cli_xarm_grip_en, SetInt16.Request(data=1), 'Habilitar Gripper xArm6'),
            (self.cli_xarm_grip_mode, SetInt16.Request(data=0), 'Configurar Gripper xArm6 a modo posición')
        ])

        self.call_services_parallel([
            #(self.cli_850_mode, SetInt16.Request(data=0), '850 a Modo 0'),
            (self.cli_xarm_mode, SetInt16.Request(data=0), 'xArm6 a Modo 0'),
            (self.cli_lin_origin, LinearMotorBackOrigin.Request(wait=True, auto_enable=True), 'Motor Lineal a Origen')
        ])

        self.call_services_parallel([
            (self.cli_lin_speed, SetInt16.Request(data=200), 'Set velocidad motor'),
            (self.cli_xarm_state, SetInt16.Request(data=0), 'Set estado Ready xArm6'),
            #(self.cli_850_state, SetInt16.Request(data=0), 'Set estado Ready uFactory 850')
        ])

        req_xarm_home = MoveJoint.Request(angles=self.xarm_initpos_angles, speed=0.35, acc=10.0, wait=True)
        req_u850_home = MoveJoint.Request(angles=self.u850_initpos_angles, speed=0.35, acc=10.0, wait=True)
        
        self.call_services_parallel([
            (self.cli_lin_pos, LinearMotorSetPos.Request(pos=self.linear_pos_scan, wait=True), 'Motor Lineal a 50mm'),
            (self.cli_xarm_joints, req_xarm_home, 'xArm6 a Home'),
            #(self.cli_850_joints, req_u850_home, 'uFactory 850 a Home'),
            (self.cli_xarm_grip_pos, GripperMove.Request(pos=800.0), 'Abrir Pinza xArm6')
        ])

        # MANTENIENDO TU ESTRUCTURA ORIGINAL DE ARGUMENTOS DIRECTOS REQ
        req_detect_xyz_xarm = MoveCartesian.Request()
        req_detect_xyz_xarm.pose = [
            self.xarm_detect_xyz[0], 
            self.xarm_detect_xyz[1], 
            self.xarm_detect_xyz[2], 
            math.radians(180), 
            0.0, 
            0.0
        ]
        req_detect_xyz_xarm.speed = 80.0
        req_detect_xyz_xarm.wait = True
        self.call_services_parallel([(self.cli_xarm_pos, req_detect_xyz_xarm, 'xArm6 a posición cartesiana de escaneo')])
        
        self.CURR_POS = [self.xarm_detect_xyz[0], self.xarm_detect_xyz[1], self.xarm_detect_xyz[2], 180.0, 0.0, 0.0]

        self.get_logger().info('Robots situados en zona de detección. Sincronizando flujos con RealSense...')
        while rclpy.ok() and self.detector is None:
            self.get_logger().info(f'{type(self.detector)}')
            self.get_logger().info('BORRACHO.')
            time.sleep(1.0)

        self.ready_grasp = True
        self.call_services_parallel([
            (self.cli_xarm_mode, SetInt16.Request(data=7), 'xArm6 Conmutando a MODO 7'),
            (self.cli_xarm_state, SetInt16.Request(data=0), 'Activando estado Ready para MODO 7')
        ])
        time.sleep(0.5)
        self.ready_check = True
        self.get_logger().info('[INIT] Secuencia completada con éxito. Celda colaborativa en ejecución.')

    def check_callback(self):
        if not self.ready_check or not self.alive: return
        x, y, z = self.CURR_POS[0], self.CURR_POS[1], self.CURR_POS[2]

        # ── 1. RETORNO POR TIMEOUT O FUERA DE RANGO ──
        if (time.monotonic() - self.last_grasp_time > 5.0 or x < self.grasping_range[0] or x > self.grasping_range[1] or y < self.grasping_range[2] or y > self.grasping_range[3]):
            if (time.monotonic() - self.last_grasp_time > 5.0 and abs(x - self.xarm_detect_xyz[0]) < 2.0 and abs(y - self.xarm_detect_xyz[1]) < 2.0):
                self.last_grasp_time = time.monotonic()
                return

            self.ready_grasp = False

            # Modificado: Petición estructurada para el plano aéreo de escaneo
            req_retorno = MoveCartesian.Request()
            req_retorno.pose = [self.xarm_detect_xyz[0], self.xarm_detect_xyz[1], self.xarm_detect_xyz[2], math.radians(180.0), 0.0, 0.0]
            req_retorno.speed = 200.0
            req_retorno.acc = 1000.0
            req_retorno.wait = True

            self.call_services_parallel([
                (self.cli_xarm_state, SetInt16.Request(data=4), 'Frenar brazo'),
                (self.cli_xarm_mode, SetInt16.Request(data=0), 'xArm6 a Modo 0'),
                (self.cli_xarm_state, SetInt16.Request(data=0), 'xArm6 Ready'),
                (self.cli_xarm_pos, req_retorno, 'Regresando a plano aéreo')
            ])
            self.pose_averager.reset()
            self.call_services_parallel([
                (self.cli_xarm_mode, SetInt16.Request(data=7), 'Reconfigurar Modo 7'),
                (self.cli_xarm_state, SetInt16.Request(data=0), 'Modo 7 Ready')
            ])
            self.GRASP_STATUS = 0
            self.ready_grasp = True
            self.last_grasp_time = time.monotonic()
            return

        # ── TRANSICIONES DE ESTADO (SEGUIMIENTO HORIZONTAL / SEGUIDOR LÍMITES) ──
        if abs(x - self.GOAL_POS[0]) < 2.0 and abs(y - self.GOAL_POS[1]) < 2.0:
            if self.GRASP_STATUS == 0:
                self.GRASP_STATUS = 1
            elif self.GRASP_STATUS == 2:
                self.GRASP_STATUS = 3

                # Modificado: Petición estructurada asíncrona para descenso dinámico
                req_descenso = MoveCartesian.Request()
                req_descenso.pose = [self.GOAL_POS[0], self.GOAL_POS[1], self.GOAL_POS[2], math.radians(self.GOAL_POS[3]), math.radians(self.GOAL_POS[4]), math.radians(self.GOAL_POS[5])]
                req_descenso.speed = 50.0
                req_descenso.acc = 1000.0
                req_descenso.wait = False
                
                self.cli_xarm_pos.call_async(req_descenso)

        # ── 2. CONDICIÓN DE DETECCIÓN Y PARADA: ENTRADA POR CONTACTO EN Z ──
        if z < self.gripper_z_mm or (z - 1.0) < self.GOAL_POS[2]:
            if not self.ready_grasp: return
            self.ready_grasp = False
            self.GRASP_STATUS = 0
            self.get_logger().info('[CONTACTO] Iniciando secuencia física de recogida y Handover...')
            
            self.call_services_parallel([
                (self.cli_xarm_state, SetInt16.Request(data=4), 'Frenar descenso'),
                (self.cli_xarm_mode, SetInt16.Request(data=0), 'Cambiar a Modo 0 Cartesiano'),
                (self.cli_xarm_state, SetInt16.Request(data=0), 'Estado Ready')
            ])

            # Modificado: Petición estructurada para la retirada vertical de seguridad
            req_elevacion = MoveCartesian.Request()
            req_elevacion.pose = [x, y, self.lift_height, math.radians(180.0), 0.0, 0.0]
            req_elevacion.speed = 100.0
            req_elevacion.acc = 1000.0
            req_elevacion.wait = True

            self.call_services_parallel([
                (self.cli_xarm_grip_pos, GripperMove.Request(pos=0.0), 'Cerrar Pinza xArm6'),
                (self.cli_xarm_pos, req_elevacion, 'Elevación vertical de seguridad')
            ])

            self.call_services_parallel([(self.cli_lin_pos, LinearMotorSetPos.Request(pos=self.linear_pos_inter, wait=True), 'Motor lineal a 700mm')])
            
            # Modificado: Petición estructurada para el viaje del xArm6 a zona de Handover común
            req_xarm_release = MoveCartesian.Request()
            req_xarm_release.pose = [self.xarm_release_xyz[0], self.xarm_release_xyz[1], self.xarm_release_xyz[2], math.radians(180.0), 0.0, 0.0]
            req_xarm_release.speed = 100.0
            req_xarm_release.acc = 1000.0
            req_xarm_release.wait = True

            # Modificado: Petición estructurada para el viaje del uFactory 850 a zona de Handover común
            req_u850_inter = MoveCartesian.Request()
            req_u850_inter.pose = [self.u850_grasp_xyz[0], self.u850_grasp_xyz[1], self.u850_grasp_xyz[2], self.u850_grasp_rpy[0], self.u850_grasp_rpy[1], self.u850_grasp_rpy[2]]
            req_u850_inter.speed = 100.0
            req_u850_inter.acc = 1000.0
            req_u850_inter.wait = True
            
            self.call_services_parallel([
                (self.cli_xarm_pos, req_xarm_release, 'xArm6 a zona común'),
                #(self.cli_850_pos, req_u850_inter, 'uFactory 850 a zona común')
            ])

            release_xyz, slot = self.get_next_free_slot()
            if slot is not None:
                req_u850_dep = MoveCartesian.Request()
                req_u850_dep.speed = 100.0
                req_u850_dep.acc = 1000.0
                req_u850_dep.wait = True

                # Modificado: Petición estructurada de depósito según el slot asignado
                if slot['row'] == 1:
                    req_u850_dep.pose = [release_xyz[0], release_xyz[1], release_xyz[2], math.radians(slot['rpy'][0]), math.radians(slot['rpy'][1]), math.radians(slot['rpy'][2])]
                else:
                    req_u850_dep.pose = [release_xyz[0], release_xyz[1] + 100.0, release_xyz[2], math.radians(slot['rpy'][0]), math.radians(slot['rpy'][1]), math.radians(slot['rpy'][2])]
                
                self.call_services_parallel([
                    # (self.cli_xarm_grip_pos, GripperMove.Request(pos=800.0), 'Abrir Pinza xArm6'),
                    # (self.cli_850_pos, req_u850_dep, 'uFactory 850 insertando en slot')
                ])
                slot['occupied'] = 1

            # Modificado: Petición estructurada para regresar el xArm6 a zona aérea de escaneo
            req_scan_pose = MoveCartesian.Request()
            req_scan_pose.pose = [self.xarm_detect_xyz[0], self.xarm_detect_xyz[1], self.xarm_detect_xyz[2], math.radians(180.0), 0.0, 0.0]
            req_scan_pose.speed = 100.0
            req_scan_pose.acc = 1000.0
            req_scan_pose.wait = True

            self.call_services_parallel([
                (self.cli_xarm_pos, req_scan_pose, 'xArm6 a zona de escaneo'),
                (self.cli_lin_pos, LinearMotorSetPos.Request(pos=self.linear_pos_scan, wait=True), 'Motor Lineal regresando a 50mm')
            ])

            self.pose_averager.reset()
            self.call_services_parallel([
                (self.cli_xarm_mode, SetInt16.Request(data=7), 'Activar Modo 7 de nuevo'),
                (self.cli_xarm_state, SetInt16.Request(data=0), 'Habilitar Servoing')
            ])
            time.sleep(1.0)
            self.ready_grasp = True
            self.last_grasp_time = time.monotonic()


def main(args=None):
    rclpy.init(args=args)
    node = CoordinadorCeldaNode()
    
    executor = MultiThreadedExecutor()
    executor.add_node(node)
    
    try:
        executor.spin()
    except KeyboardInterrupt:
        pass
    finally:
        node.alive = False
        node.destroy_node()
        if rclpy.ok(): rclpy.shutdown()

if __name__ == '__main__':
    main()