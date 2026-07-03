#!/usr/bin/env python3
"""
coordinador_xarm_motorlin_850.py
====================
Orquestador de Celda Colaborativa en ROS 2. Integración de la cinemática
del uFactory 850, xArm6, el Motor Lineal y el procesador de visión por momentos.
"""

import rclpy
import time
import math
import numpy as np
from rclpy.node import Node

# Interfaces de servicio nativas de xarm_msgs
from xarm_msgs.srv import (
    SetInt16,
    SetInt16ById,
    LinearMotorSetPos,
    LinearMotorBackOrigin,
    MoveCartesian,
    MoveJoint,
    GripperMove,
)

# Importaciones del módulo de visión localizados en tu paquete ROS 2
from tfm_martin.camera.rs_camera import RealSenseCamera
from tfm_martin.cv_grasp_detector import CVGraspDetector
from tfm_martin.helpers.matrix_funcs import euler2mat, convert_pose
from tf2_ros import TransformException
from tf2_ros.buffer import Buffer
from tf2_ros.transform_listener import TransformListener

# PARAMETROS GLOBALES DE MOVIMIENTO
LINEAR_SPEED       = 200    # mm/s
LINEAR_POS_DETECT  = 60    # mm
LINEAR_POS_RELEASE = 650    # mm

class CoordinadorCeldaNode(Node):

    def __init__(self):
        super().__init__('coordinador_celda_node')
        self.get_logger().info('Inicializando Orquestador de Celda Colaborativa (ROS 2)...')

        # ── 1. CONFIGURACIÓN GEOMÉTRICA DE TUS SCRIPTS ORIGINALES ──────────────
        # Parámetros del xArm6 + Motor Lineal
        self.xarm_initpos_angles = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  # Ángulos de inicio del xArm6 (en radianes)
        self.xarm_detect_xyz  = [220.5, 0.0, 575.0]
        self.xarm_release_xyz = [0.0, 360.5, 488.0]
        self.linear_pos_scan  = 70
        self.linear_pos_inter = 700
        
        # Parámetros del uFactory 850 y xArm-6(Puntos fijos extraídos de tus scripts)
        self.u850_initpos_angles = [0.0, 0.0, math.radians(-45.0), 0.0, math.radians(-45.0), 0.0]  # Ángulos de inicio del uFactory 850 (en radianes)
        self.u850_grasp_xyz   = [575.1, 23.2, 590.0]  # Punto físico común de Handover
        self.u850_grasp_rpy   = [math.radians(90), 0.0, math.radians(90)]
        
        # Slots de Depósito (Estructura de celdas para el uFactory 850)
        self.deposit_slots = [
            {'xyz': [57.8, -644.6, 650.0],  'rpy': [180.0, 0.0, 0.0], 'occupied': 0, 'row': 1, 'column': 1},
            {'xyz': [215.7, -644.6, 650.0], 'rpy': [180.0, 0.0, 0.0], 'occupied': 0, 'row': 1, 'column': 2},
            {'xyz': [56.9, -484.9, 361.0],  'rpy': [-152.0, -87.8, -116.3], 'occupied': 0, 'row': 2, 'column': 1},
            {'xyz': [207.3, -484.9, 361.0], 'rpy': [-152.0, -87.8, -116.3], 'occupied': 0, 'row': 2, 'column': 2},
        ]
        self.container_xyz = [300.0, 300.0, 370.0]

        # ── 2. CLIENTES ROS 2 ──────────────────────────────────────────────────
        # xArm6 + Motor Lineal
        self.cli_lin_enable  = self.create_client(SetInt16, '/xarm/set_linear_motor_enable')
        self.cli_lin_speed   = self.create_client(SetInt16, '/xarm/set_linear_motor_speed')
        self.cli_lin_origin  = self.create_client(LinearMotorBackOrigin, '/xarm/set_linear_motor_back_origin')
        self.cli_lin_pos     = self.create_client(LinearMotorSetPos, '/xarm/set_linear_motor_pos')
        self.cli_xarm_mode   = self.create_client(SetInt16, '/xarm/set_mode')
        self.cli_xarm_state  = self.create_client(SetInt16, '/xarm/set_state')
        self.cli_xarm_pos    = self.create_client(MoveCartesian, '/xarm/set_position')
        self.cli_xarm_joints  = self.create_client(MoveJoint, '/xarm/set_servo_angle')
        self.cli_xarm_enable = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.cli_xarm_grip_en   = self.create_client(SetInt16, '/xarm/set_gripper_enable')
        self.cli_xarm_grip_mode = self.create_client(SetInt16, '/xarm/set_gripper_mode')
        self.cli_xarm_grip_pos  = self.create_client(GripperMove, '/xarm/set_gripper_position')

        # uFactory 850
        self.cli_850_mode    = self.create_client(SetInt16, '/ufactory/set_mode')
        self.cli_850_state   = self.create_client(SetInt16, '/ufactory/set_state')
        self.cli_850_pos     = self.create_client(MoveCartesian, '/ufactory/set_position')
        self.cli_850_joints  = self.create_client(MoveJoint, '/ufactory/set_servo_angle')
        self.cli_850_enable  = self.create_client(SetInt16ById, '/ufactory/motion_enable')

        self._wait_all_services()

        # ── 3. SUBSISTEMA DE VISIÓN EN BEBEDO ─────────────────────────────────
        self.camera = RealSenseCamera(width=640, height=480, serial_number='231122070195')
        color_intrin, _ = self.camera.get_intrinsics(align=True)
        self.camera_k = np.array([
            [color_intrin.fx, 0,               color_intrin.ppx],
            [0,               color_intrin.fy,  color_intrin.ppy],
            [0,               0,               1               ]
        ])
        
        detector_config = {'OPEN_LOOP_HEIGHT': 340, 'GGCNN_IN_THREAD': False, 'DEPTH_CAM_K': self.camera_k}
        self.detector = CVGraspDetector(detector_config, None, None)

        # ── CONFIGURACIÓN DE CALIBRACIÓN OJO-MANO EXTRAÍDA DE TU ARCHIVO REAL ──
        self.gripper_z_mm             = 150.0  # Offset real del gripper (GRIPPER_Z_MM)
        self.tf_buffer = Buffer()
        self.tf_listener = TransformListener(self.tf_buffer, self)
        self.get_logger().info("Escuchador TF2 para ROS 2 Jazzy inicializado correctamente.")

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
            (self.cli_850_mode,    '/ufactory/set_mode'),
            (self.cli_850_state,   '/ufactory/set_state'),
            (self.cli_850_pos,     '/ufactory/set_position'),
            (self.cli_850_joints,  '/ufactory/set_servo_angle'),
            (self.cli_850_enable,  '/ufactory/motion_enable'),
        ]
        for client, name in services:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Esperando servicio crítico {name}...')

    def call_services_parallel(self, calls: list[tuple]) -> list:
        futures = []
        for client, request, label in calls:
            self.get_logger().info(f'  → Ejecutando: {label}')
            futures.append((client.call_async(request), label))

        results = []
        for future, label in futures:
            rclpy.spin_until_future_complete(self, future)
            results.append(future.result())
        return results

    def get_next_free_slot(self):
        """Lógica de asignación de baldas del script robot_grasp_850.py"""
        for slot in self.deposit_slots:
            if slot['occupied'] == 0:
                return slot['xyz'], slot
        return self.container_xyz, None

    def obtener_pose_dinamica_vision(self):
        """Interroga al CVGraspDetector"""
        color_image, depth_image = self.camera.get_images(align=True)
        self.detector._color_img = color_image
        robot_z = self.xarm_detect_xyz[2] / 1000.0   # convierte mm a metros
        _, result = self.detector.get_grasp_img(depth_image, self.camera_k, robot_z)
        return result
    
    def calcular_coordenadas_objeto(self, cx, cy, depth_image, camera_intrinsics):
        """
        Toma los píxeles (cx, cy) del detector, los convierte a metros con la RealSense
        y los transforma a milímetros respecto a la base del xArm usando TF2 en Jazzy.
        """
        # 1. Obtener la profundidad en metros en el centro del objeto
        z_metros = depth_image[int(cy), int(cx)]
        
        if np.isnan(z_metros) or z_metros <= 0:
            self.get_logger().warn("Profundidad inválida en el centro del objeto.")
            return None

        # 2. Desproyección usando el modelo Pin-hole e intrínsecos de rs_camera.py
        fx = camera_intrinsics.fx
        fy = camera_intrinsics.fy
        ppx = camera_intrinsics.ppx
        ppy = camera_intrinsics.ppy

        x_cam = (cx - ppx) * z_metros / fx
        y_cam = (cy - ppy) * z_metros / fy
        z_cam = z_metros

        # 3. Transformar de 'camera_color_frame' (Cámara) a 'link_base' (Robot xArm)
        try:
            now = rclpy.time.Time()
            # Jazzy calcula la unión: link_base -> link_eef -> camera_color_frame de forma nativa
            trans = self.tf_buffer.lookup_transform(
                'link_base', 
                'camera_color_frame', 
                now, 
                timeout=rclpy.duration.Duration(seconds=1.0)
            )
            
            # Posición de la cámara según ROS 2
            tx = trans.transform.translation.x
            ty = trans.transform.translation.y
            tz = trans.transform.translation.z

            # Proyección final combinando los metros de la cámara con la posición del robot
            # (Aproximación directa si los ejes de rotación de la cámara están alineados al eef)
            x_robot_mm = (tx + x_cam) * 1000.0
            y_robot_mm = (ty + y_cam) * 1000.0
            z_robot_mm = (tz + z_cam) * 1000.0

            return [x_robot_mm, y_robot_mm, z_robot_mm]

        except TransformException as ex:
            self.get_logger().error(f"No se pudo resolver la transformada en Jazzy: {ex}")
            return None

    # ── 2. FLUJO DE TRABAJO COLABORATIVO UNIFICADO ─────────────────────────
    def run_cell_process(self):
        # INITS GENERALES (Modo 0, State 0 y Energización)
        self.get_logger().info('PASO 1: Habilitar los robots xArm6 + Motor lineal y uFactory 850...')
        req_lin_en = SetInt16.Request(); req_lin_en.data = 1
        req_xarm_en = SetInt16ById.Request(); req_xarm_en.id = 8; req_xarm_en.data = 1
        req_850_en = SetInt16ById.Request(); req_850_en.id = 8; req_850_en.data = 1
        req_grip_en   = SetInt16.Request(); req_grip_en.data = 1    
        req_grip_mode = SetInt16.Request(); req_grip_mode.data = 0
        
        self.call_services_parallel([
            (self.cli_lin_enable, req_lin_en, 'Habilitar Motor Lineal'),
            (self.cli_xarm_enable, req_xarm_en, 'Habilitar xArm6'),
            (self.cli_850_enable, req_850_en, 'Habilitar uFactory 850'),
            (self.cli_xarm_grip_en, req_grip_en, 'Habilitar Gripper xArm6'),
            (self.cli_xarm_grip_mode, req_grip_mode, 'Configurar Gripper xArm6 a modo de posición')
        ])
        time.sleep(0.75)

        # Modos y estados de tipo de movimientos de los xArm6 y ufactory 850
        self.get_logger().info('PASO 2: Configurando modos y estados de movimiento...')
        req_xarm_mode   = SetInt16.Request(); req_xarm_mode.data = 0  # <-- Activa el modo servoing cartesiano en tiempo real
        req_u850_mode   = SetInt16.Request(); req_u850_mode.data   = 0  # Modo Cartesiano de fábrica
        req_origin = LinearMotorBackOrigin.Request(); req_origin.wait = True; req_origin.auto_enable = True
        
        self.call_services_parallel([
            (self.cli_850_mode, req_u850_mode, '850 a Modo Articular/Cartesiano'),
            (self.cli_xarm_mode, req_xarm_mode, 'xArm6 a Modo Articular/Cartesiano'),
            (self.cli_lin_origin, req_origin, 'Motor Lineal a Origen')
        ])

        # Configurar velocidades iniciales de trabajo y estado del brazo robotico
        req_lin_speed = SetInt16.Request(); req_lin_speed.data = LINEAR_SPEED
        req_xarm_state  = SetInt16.Request(); req_xarm_state.data = 0   # Estado Ready para moverse
        req_850_state  = SetInt16.Request(); req_850_state.data = 0   # Estado Ready para moverse
        
        self.call_services_parallel([
            (self.cli_lin_speed, req_lin_speed, 'Set velocidad motor'),
            (self.cli_xarm_state, req_xarm_state, 'Set estado xArm6'),
            (self.cli_850_state, req_850_state, 'Set estado uFactory 850')
        ])
        
        # POSICIONAMIENTO INICIAL DE LOS ROBOTS (xArm6 y uFactory 850)
        self.get_logger().info('PASO 3: Moviendo robots a posiciones iniciales...')
        req_xarm_home = MoveJoint.Request()
        req_xarm_home.angles = self.xarm_initpos_angles
        req_xarm_home.speed  = 0.35
        req_xarm_home.acc    = 10.0
        req_xarm_home.wait   = True
        req_u850_home = MoveJoint.Request()
        req_u850_home.angles = self.u850_initpos_angles
        req_u850_home.speed  = 0.35
        req_u850_home.acc    = 10.0
        req_u850_home.wait   = True
        req_open_gripper = GripperMove.Request()
        req_open_gripper.pos = 850.0 

        self.call_services_parallel([
            (self.cli_xarm_joints, req_xarm_home, 'xArm6 a Posición Inicial'),
            (self.cli_850_joints, req_u850_home, 'uFactory 850 a Posición Inicial'),
            (self.cli_xarm_grip_pos, req_open_gripper, 'Abrir Gripper xArm6')
        ])

        while rclpy.ok():
            # ETAPA 1: Ir a escaneo (Motor en po# ── AÑADIR ESTE BLOQUE AQUÍ: CONMUTACIÓN A MODO 7 ANTES DE LEER LA CÁMARA ──
            self.get_logger().info('=== INICIANDO NUEVO CICLO COOPERATIVO ===')

            # ETAPA 1: Ir a escaneo (Motor en po# ── AÑADIR ESTE BLOQUE AQUÍ: CONMUTACIÓN A MODO 7 ANTES DE LEER LA CÁMARA ──
            req_lin_scan = LinearMotorSetPos.Request(); req_lin_scan.pos = self.linear_pos_scan; req_lin_scan.speed = 200; req_lin_scan.wait = True
            req_xarm_scan = MoveCartesian.Request()
            req_xarm_scan.pose = [self.xarm_detect_xyz[0], self.xarm_detect_xyz[1], self.xarm_detect_xyz[2], math.radians(180), 0.0, 0.0]
            req_xarm_scan.speed = 120.0; req_xarm_scan.wait = True

            self.call_services_parallel([
                (self.cli_lin_pos, req_lin_scan, 'Motor Lineal a zona escaneo'),
                (self.cli_xarm_pos, req_xarm_scan, 'xArm6 a posición de escaneo')
            ])
            time.sleep(1.0)

            ##########################################################################
            # ── MODO 7: SERVOING DINÁMICO EN 3 FASES (XY → ÁNGULO → Z) ──────────────
            ##########################################################################
            self.get_logger().info('[MODO 7] Activando Servoing dinámico para seguimiento...')

            req_switch_m7 = SetInt16.Request(); req_switch_m7.data = 7
            req_state_m7  = SetInt16.Request(); req_state_m7.data  = 0

            self.call_services_parallel([
                (self.cli_xarm_mode,  req_switch_m7, 'Conmutando a MODO 7'),
                (self.cli_xarm_state, req_state_m7,  'Activando estado Ready para MODO 7'),
            ])
            time.sleep(0.4)

            # ── Parámetros de control de las fases ──────────────────────────────────
            MAX_ITERATIONS     = 150
            XY_ALIGN_THRESH_M  = 0.003   # 3 mm
            ANG_ALIGN_THRESH   = math.radians(4)
            SAFE_Z_MM          = self.xarm_detect_xyz[2]
            GRASP_Z_THRESHOLD  = self.gripper_z_mm + 15.0 # Umbral de parada física
            LOOP_SLEEP         = 0.05    # 50ms (Muestreo rápido continuo en el descenso)

            FASE_XY    = 'XY'
            FASE_ANG   = 'ANGULO'
            FASE_DESC  = 'DESCENSO'
            fase_actual = FASE_XY

            curr_xarm_xyz = list(self.xarm_detect_xyz)
            curr_ang      = 0.0
            grasp_reached = False
            iteration = 0

            while rclpy.ok() and not grasp_reached and iteration < MAX_ITERATIONS:
                # 1. Captura de imagen e interrogación al detector
                result_cam = self.obtener_pose_dinamica_vision()
                if not result_cam:
                    time.sleep(LOOP_SLEEP)
                    iteration += 1
                    continue

                x_cam, y_cam, z_cam, ang_b = result_cam[0], result_cam[1], result_cam[2], result_cam[3]

                # 2. Consultar el árbol TF dinámico de ROS 2 Jazzy
                try:
                    now = rclpy.time.Time()
                    trans = self.tf_buffer.lookup_transform(
                        'link_base', 'camera_color_frame', now,
                        timeout=rclpy.duration.Duration(seconds=0.1)
                    )
                    tx = trans.transform.translation.x
                    ty = trans.transform.translation.y
                    tz = trans.transform.translation.z

                    target_x = (tx + x_cam) * 1000.0
                    target_y = (ty + y_cam) * 1000.0
                    target_z = (tz - z_cam) * 1000.0 + self.gripper_z_mm
                    ang_target = ang_b + math.pi / 2

                except TransformException:
                    time.sleep(LOOP_SLEEP)
                    iteration += 1
                    continue

                # ── FASE 1: Centrar XY de forma estricta (Bloqueante) ──────────────────
                if fase_actual == FASE_XY:
                    self.get_logger().info(f'[FASE XY][Iter {iteration}] Centrando sobre el objetivo...')
                    req = MoveCartesian.Request()
                    req.pose  = [target_x, target_y, SAFE_Z_MM, math.radians(180), 0.0, 0.0]
                    req.speed = 100.0
                    req.wait  = True # Asegura llegar físicamente antes de calcular rotación
                    
                    future = self.cli_xarm_pos.call_async(req)
                    rclpy.spin_until_future_complete(self, future)

                    curr_xarm_xyz = [target_x, target_y, SAFE_Z_MM]
                    fase_actual = FASE_ANG

                # ── FASE 2: Ajustar Ángulo de la muñeca (Bloqueante) ──────────────────
                elif fase_actual == FASE_ANG:
                    self.get_logger().info(f'[FASE ÁNGULO][Iter {iteration}] Alineando orientación de la pinza...')
                    req = MoveCartesian.Request()
                    req.pose  = [curr_xarm_xyz[0], curr_xarm_xyz[1], SAFE_Z_MM, math.radians(180), 0.0, ang_target]
                    req.speed = 80.0
                    req.wait  = True # Espera a completar el giro de la articulación 6
                    
                    future = self.cli_xarm_pos.call_async(req)
                    rclpy.spin_until_future_complete(self, future)

                    curr_ang = ang_target
                    fase_actual = FASE_DESC
                    self.get_logger().info('[FASE DESCENSO] Iniciando bajada guiada por visión continua...')

                # ── FASE 3: Descenso Reactivo y Continuo en Z (Asíncrono fluido) ──────
                elif fase_actual == FASE_DESC:
                    # Condición de parada real basada en la posición actual reportada o calculada
                    # Si target_z cae por debajo de la altura física del objeto, detenemos el bucle
                    if target_z <= GRASP_Z_THRESHOLD:
                        self.get_logger().info(f'[FASE DESCENSO] Umbral de contacto alcanzado: Z={target_z:.1f}mm')
                        
                        # Comando de detención de trayectoria inmediato mediante cambio de estado
                        self.cli_xarm_state.call_async(SetInt16.Request(data=4))
                        time.sleep(0.1)
                        
                        # Retornar a Modo 0 fijo para asegurar el agarre estable
                        self.cli_xarm_mode.call_async(SetInt16.Request(data=0))
                        self.cli_xarm_state.call_async(SetInt16.Request(data=0))
                        time.sleep(0.1)
                        
                        grasp_reached = True
                        break

                    # Si aún no ha llegado, inyecta el comando de descenso asíncronamente a 20 FPS (50ms)
                    # permitiendo que el robot baje de forma fluida y corrija pequeñas desviaciones
                    req = MoveCartesian.Request()
                    req.pose  = [curr_xarm_xyz[0], curr_xarm_xyz[1], target_z, math.radians(180), 0.0, curr_ang]
                    req.speed = 40.0 # Velocidad suave para evitar impactos bruscos
                    req.wait  = False # <--- IMPORTANTE: Asíncrono para permitir refresco dinámico
                    self.cli_xarm_pos.call_async(req)

                iteration += 1
                time.sleep(LOOP_SLEEP)

            # ── Comprobación de seguridad al salir del bucle ──────────────────────────
            if not grasp_reached:
                self.get_logger().warn('Bucle de visión abortado por límite de iteraciones. Cancelando ciclo.')
                return

            # ── EJECUCIÓN REAL DEL PICK ───────────────────────────────────────────────
            self.get_logger().info('[PICK] Cerrando pinza de forma segura sobre la pelota...')
            req_close = GripperMove.Request()
            req_close.pos = 0.0 # Cierre total de la pinza (Ajusta según las dimensiones de tu garra)
            future_grip = self.cli_xarm_grip_pos.call_async(req_close)
            rclpy.spin_until_future_complete(self, future_grip)
            time.sleep(1.0) # Margen de espera físico para consolidar la presión de agarre

            # ETAPA 4: TRANSFERENCIA INTERMEDIA SIMULTÁNEA (HANDOVER)
            # ... [Tu código de aproximación del uFactory 850 permanece intacto aquí abajo] ...

            # ETAPA 4: TRANSFERENCIA INTERMEDIA SIMULTÁNEA (HANDOVER)
            # El motor lineal se estira a 700 mm y el xArm se coloca en la pose intermedia.
            req_lin_inter = LinearMotorSetPos.Request(); req_lin_inter.pos = self.linear_pos_inter; req_lin_inter.speed = 200; req_lin_inter.wait = True
            req_xarm_inter = MoveCartesian.Request()
            req_xarm_inter.pose = [self.xarm_release_xyz[0], self.xarm_release_xyz[1], self.xarm_release_xyz[2], math.radians(180), 0.0, 0.0]
            req_xarm_inter.speed = 150.0; req_xarm_inter.wait = True

            # Simultáneamente, el uFactory 850 se desplaza al mismo punto de encuentro para recogerlo
            req_u850_inter = MoveCartesian.Request()
            req_u850_inter.pose = [self.u850_grasp_xyz[0], self.u850_grasp_xyz[1], self.u850_grasp_xyz[2], self.u850_grasp_rpy[0], self.u850_grasp_rpy[1], self.u850_grasp_rpy[2]]
            req_u850_inter.speed = 100.0; req_u850_inter.wait = True

            self.get_logger().info('Lanzando aproximación simultánea al punto intermedio colaborativo...')
            self.call_services_parallel([
                (self.cli_lin_pos, req_lin_inter, 'Motor Lineal extendiéndose (700mm)'),
                (self.cli_xarm_pos, req_xarm_inter, 'xArm6 a zona común'),
                (self.cli_850_pos, req_u850_inter, 'uFactory 850 a zona común')
            ])

            # [AQUÍ INTERCAMBIAS LAS SEÑALES DE APERTURA/CIERRE DE PINZA ENTRE ROBOTS]
            self.get_logger().info('Robots sincronizados en punto central. Pieza transferida.')
            time.sleep(1.0)

            # ETAPA 5: DEPÓSITO COORDENADO EN BALDA INTERMANUAL
            release_xyz, slot = self.get_next_free_slot()
            if slot is None:
                self.get_logger().info('Slots de balda llenos. Terminando orquestación.')
                break

            req_u850_dep = MoveCartesian.Request()
            # Si es Fila 1, aproximación directa por arriba como especificaba tu script original
            if slot['row'] == 1:
                req_u850_dep.pose = [release_xyz[0], release_xyz[1], release_xyz[2], math.radians(slot['rpy'][0]), math.radians(slot['rpy'][1]), math.radians(slot['rpy'][2])]
            else:
                # Fila 2: Inserción por aproximación de muñeca rotada
                req_u850_dep.pose = [release_xyz[0], release_xyz[1] + 100.0, release_xyz[2], math.radians(slot['rpy'][0]), math.radians(slot['rpy'][1]), math.radians(slot['rpy'][2])]
            
            req_u850_dep.speed = 100.0; req_u850_dep.wait = True
            
            self.get_logger().info(f'uFactory 850 depositando en fila {slot["row"]}, columna {slot["column"]}...')
            self.call_services_parallel([(self.cli_850_pos, req_u850_dep, 'uFactory 850 insertando en slot')])
            
            # [AQUÍ ABRES LA PINZA DEL 850]
            slot['occupied'] = 1
            time.sleep(1.0)

def main(args=None):
    rclpy.init(args=args)
    node = CoordinadorCeldaNode()
    try:
        node.run_cell_process()
    except KeyboardInterrupt:
        pass
    node.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()