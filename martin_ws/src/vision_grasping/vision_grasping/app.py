import math

import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from sensor_msgs.msg import Image, CameraInfo
from xarm_msgs.srv import MoveCartesian
from xarm_msgs.srv import GetFloat32List
from xarm_msgs.srv import GetFloat32
from xarm_msgs.msg import RobotMsg

import time
import numpy as np
import cv2
from cv_bridge import CvBridge
from queue import Queue

from .settings import (WIN_NAME, 
                       CAM_HEIGHT, 
                       CAM_WIDTH, 
                       OPEN_LOOP_HEIGHT, 
                       GGCNN_IN_THREAD,
                       SHOW_GRASP_IMG,
                       EULER_EEF_TO_COLOR_OPT,
                       EULER_COLOR_TO_DEPTH_OPT,
                       GRASPING_RANGE,
                       DETECT_XYZ,
                       RELEASE_XYZ,
                       LIFT_OFFSET_Z,
                       GRIPPER_Z_MM,
                       GRASPING_MIN_Z
                       )
from .cv_grasp_detector import DEPTH_VALID_MIN, CVGraspDetector
from .utils import (compute_crop_and_intrinsics, 
                    get_combined_img,
                    compute_goal_pose)

class GraspDetectorNode(Node):
    def __init__(self):
        super().__init__('grasp_detector_node')

        self.get_logger().info('Nodo vision_grasping iniciado.')

        self.cb_group = ReentrantCallbackGroup()

        self.last_cmd_time = 0.0
        self.cmd_interval = 0.05   # 20 FPS

        # --- Robots ---
        self.xarm6_pose = [220.5, 0.0, 575.0, math.radians(180), 0.0, 0.0] #None
        self.get_logger().info(f'Pose XArm6: {self.xarm6_pose}')
        self.uf850_pose = None
        self.xarm6_state = None
        self.xarm6_last_state = 0

        # --- Colas internas del detector ---
        self.depth_img_que = Queue(1)
        self.ggcnn_cmd_que = Queue(1)

        # --- Estado ---
        self.depth_camera_k = None
        self.detector_initialized = False
        self.grasp_detector = None
        self.INIT_STATUS = True
        self.GRASP_STATUS = 0
        self.GOAL_POS = None
        self.CURR_POS = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
        self.gripper_position = 850.0

        # --- CV Bridge ---
        self.bridge = CvBridge()

        # --- Camera ---
        self.depth_image = None
        self.color_image = None
        self.crop_size = None
        self.crop_x_inx = None
        self.crop_y_inx = None
        self.depth_camera_k_crop = None

        # -----------------------------
        # --- TIMERS ---
        # -----------------------------
        self.create_timer(0.05, 
                          self.process_frame,
                          callback_group=self.cb_group)  # 20 FPS
        
        self.grasp_debug_image_pub = self.create_publisher(Image, 
                                               '/grasp/debug_image', 
                                               10)


        # -----------------------------
        # --- SUSCRIPCIONES ---
        # -----------------------------

        self.create_subscription(
            RobotMsg,
            '/xarm/robot_states',
            self.robot_states_callback,
            10,
            callback_group=self.cb_group
        )
        
        # Intrinsecas del depth (profundidad)
        self.create_subscription(
            CameraInfo,
            '/camera/camera/aligned_depth_to_color/camera_info',
            self.depth_camera_info_callback,
            10,
            callback_group=self.cb_group
        )

        # Imagen de depth (profundidad)
        self.create_subscription(
            Image,
            '/camera/camera/aligned_depth_to_color/image_raw',
            self.depth_camera_image_callback,
            10,
            callback_group=self.cb_group
        )

        # Imagen de color (RGB)
        self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.color_camera_image_callback,
            10,
            callback_group=self.cb_group
        )

        self.get_logger().info('Esperando CameraInfo del depth...')

        # -----------------------------
        # --- SERVICIOS ---
        # -----------------------------

        # Posicion cartesiana del robot:
        # posicion mm (3) + orientacion rad (3) 
        self.xarm6_pos_client = self.create_client(
            GetFloat32List,
            '/xarm/get_position',
            callback_group=self.cb_group
        )

        """self.uf850_pos_client = self.create_client(
            GetFloat32List,
            '/ufactory/get_position',
            callback_group=self.cb_group
        )"""
        
        # Esperar a que el servicio esté disponible
        #while not self.robot_pos_client.wait_for_service(timeout_sec=1.0):
        #    self.get_logger().warn('Esperando servicio /ufactory/get_position...')

        # Movimiento cartesiano (en espacio de la tarea)
        self.moveit_client = self.create_client(MoveCartesian, 
                                                '/xarm/set_position')
        #while not self.moveit_client.wait_for_service(timeout_sec=1.0):
        #    self.get_logger().warn("Esperando servicio /xarm/set_position...")

        #self.set_xarm6_position(DETECT_XYZ_RPY)  # Ir a la posición inicial de detección
        #self.get_xarm6_position()

        self.euler_eef_to_color_opt = EULER_EEF_TO_COLOR_OPT
        self.euler_color_to_depth_opt = EULER_COLOR_TO_DEPTH_OPT
        self.gripper_z_mm = GRIPPER_Z_MM
        self.grasping_min_z = GRASPING_MIN_Z
        self.grasping_range = GRASPING_RANGE
        self.min_result_z = DEPTH_VALID_MIN
        
        # Mapeos requeridos en perform_grasp_sequence
        self.detect_x, self.detect_y, self.detect_z = DETECT_XYZ[0], DETECT_XYZ[1], DETECT_XYZ[2]
        self.release_x, self.release_y, self.release_z = RELEASE_XYZ[0], RELEASE_XYZ[1], RELEASE_XYZ[2]

        # Flag de control para evitar ejecuciones concurrentes de la secuencia física
        self.is_moving = False





    # ----------------------------------------------------------------------
    # --- CALLBACKS ---
    # ----------------------------------------------------------------------
    def robot_states_callback(self, msg: RobotMsg):
        self.xarm6_last_state = self.xarm6_state
        self.xarm6_state = msg.state  # 1: RUNNING, 2: SLEEPING

        # Extraer posición TCP actual (Pasando la orientación de Radianes a Grados)
        curr_x = msg.pose[0]
        curr_y = msg.pose[1]
        curr_z = msg.pose[2]
        curr_roll = math.degrees(msg.pose[3])
        curr_pitch = math.degrees(msg.pose[4])
        curr_yaw = math.degrees(msg.pose[5])
        
        self.CURR_POS = [curr_x, curr_y, curr_z, curr_roll, curr_pitch, curr_yaw]

        # Secuencia de inicialización: cuando el robot pasa de 1: RUNNING a 2: SLEEPING por primera vez, se considera que la inicialización ha terminado
        if self.xarm6_last_state == 1 and self.xarm6_state == 2 and self.INIT_STATUS == True:
            self.INIT_STATUS = False

        # Si no hay un objetivo de agarre fijado por la cámara, salimos
        if self.GOAL_POS is None:
            return

        # --- MÁQUINA DE ESTADOS REACTIVA POR FASES ---
        # Si el robot ha llegado a centrarse horizontalmente sobre el objeto (Tolerancia de 2mm)
        if abs(curr_x - self.GOAL_POS[0]) < 2.0 and abs(curr_y - self.GOAL_POS[1]) < 2.0:
            if self.GRASP_STATUS == 0:
                self.GRASP_STATUS = 1
        #     elif self.GRASP_STATUS == 1:
        #         self.GRASP_STATUS = 2
        #     elif self.GRASP_STATUS == 2:
        #         # --- FASE 2: ORDENAR EL DESCENSO EN Z ---
        #         self.get_logger().info("Alineación XY alcanzada. Bajando verticalmente en Z hacia el objeto...")
        #         self.GRASP_STATUS = 3
                
        #         # Enviamos el objetivo completo (utilizando ahora sí la Z de agarre real en el fondo)
        #         self.set_xarm6_position_async(self.GOAL_POS, speed=50.0)

        # # --- FASE 3: DETECCIÓN DE FIN DE MOVIMIENTO EN EL FONDO ---
        # # Si el brazo termina de moverse (pasa de 1: RUNNING a 2: SLEEPING) en pleno descenso (Estado 3)
        # if self.xarm6_last_state == 1 and self.xarm6_state == 2 and self.GRASP_STATUS == 3:
        #     self.get_logger().info("¡Robot en posición de fondo! Cerrando pinza sobre la pieza...")
        #     self.GRASP_STATUS = 4
            
        #     # TODO: Añade aquí tu llamada al servicio para cerrar el gripper físicamente
        #     # p.ej: self.call_gripper_service(position=0)

        # # --- FASE 4: CONDICIÓN DE AGARRE EFECTIVO Y RETIRADA ---
        # # Si la pinza está en proceso de agarre y detectamos que cerró por debajo del umbral de 200
        # if self.GRASP_STATUS == 4 and self.gripper_position < 200.0:
        #     self.get_logger().info("Objeto asegurado en el gripper. Elevando el brazo...")
        #     self.GRASP_STATUS = 5
            
        #     # Calculamos una Z alta sumando 100mm a la posición vertical actual
        #     z_retirada = curr_z + 100.0
        #     escape_pose = [curr_x, curr_y, z_retirada, 180.0, 0.0, curr_yaw]
            
        #     self.set_xarm6_position_async(escape_pose, speed=80.0)




        

        # if self.xarm6_last_state == 1 and self.xarm6_state == 2 and self.GRASP_STATUS == 0:
        #     self.GRASP_STATUS = 1

        # self.get_logger().info(f'Pose XArm6 recibida: {self.xarm6_pose}')


    # Callback de la informacion de la cámara de profundidad:
    # inicializa el detector cuando llega el primer CameraInfo
    def depth_camera_info_callback(self, msg: CameraInfo):
        if self.detector_initialized:
            return

        # Construir matriz intrínseca DEPTH_CAM_K solo la primera vez
        k = msg.k  # lista de 9 elementos
        self.depth_camera_k = np.array([
            [k[0], k[1], k[2]],
            [k[3], k[4], k[5]],
            [k[6], k[7], k[8]],
        ])

        self.get_logger().info(f'Intrínsecas recibidas:\n{self.depth_camera_k}')

        # Configuración para CVGraspDetector
        detector_config = {
            'OPEN_LOOP_HEIGHT': OPEN_LOOP_HEIGHT,
            'GGCNN_IN_THREAD':  GGCNN_IN_THREAD,
            'DEPTH_CAM_K':      self.depth_camera_k,
        }

        # Inicializar detector
        self.grasp_detector = CVGraspDetector(
            detector_config,
            self.depth_img_que,
            self.ggcnn_cmd_que
        )

        self.detector_initialized = True
        if self.grasp_detector is not None:
            self.get_logger().info('CVGraspDetector inicializado correctamente.')


    # Callback de la imagen de la cámara de profundidad
    def depth_camera_image_callback(self, msg: Image):
        depth = self.bridge.imgmsg_to_cv2(msg, desired_encoding='passthrough')
        #self.depth_image = depth

        # RealSense ROS2 publica depth en mm (uint16)
        if depth.dtype == np.uint16:
            depth = depth.astype(np.float32) / 1000.0

        self.get_logger().info(
            f"dtype={depth.dtype}, "
            f"min={depth.min():.3f}, "
            f"max={depth.max():.3f}, "
            f"center={depth[240,320]:.3f}"
        )

        self.depth_image = depth

        # Se actualizan las k solo la primera vez
        if self.crop_size is None and self.depth_camera_k is not None:
            (self.crop_size,
            self.crop_x_inx,
            self.crop_y_inx,
            self.depth_camera_k_crop) = compute_crop_and_intrinsics(
                depth,
                self.depth_camera_k
            )

            self.get_logger().info(f'Crop inicializado: size={self.crop_size}')
            self.get_logger().info(f'Intrínsecas recortadas:\n{self.depth_camera_k_crop}')


    # Callback de la imagen de la cámara de color
    def color_camera_image_callback(self, msg):
        self.color_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')


    # Callback del procesamiento de vision (depth + color)
    def process_frame(self):
        if True: #self.INIT_STATUS == False:
            #self.get_logger().info('NO ESTOY EN INICIO, DEBERIA IR A LA PELOTA')
            if self.color_image is None or self.depth_image is None:
                #self.get_logger().info('NO COLOR IMAGE')
                return
            if self.crop_size is None:
                #self.get_logger().info('NO CROP SIZE')
                return
    

            # self.get_logger().info('process_frame ejecutado')

            # Recortar color y depth
            color_crop = self.color_image[
                self.crop_y_inx:self.crop_y_inx + self.crop_size,
                self.crop_x_inx:self.crop_x_inx + self.crop_size,
            ]

            depth_crop = self.depth_image[
                self.crop_y_inx:self.crop_y_inx + self.crop_size,
                self.crop_x_inx:self.crop_x_inx + self.crop_size,
            ]

            # Pasar color al detector
            self.grasp_detector._color_img = color_crop

            # Obtener posicion del robot
            #self.get_xarm6_position()

            if self.xarm6_pose is not None:
                #self.get_logger().info('ENTRO EN XARM6 POSE')
                # Identificación y reconocimiento de la pelota
                grasp_img, result = self.grasp_detector.get_grasp_img(
                    depth_crop,
                    self.depth_camera_k_crop,
                    self.xarm6_pose[2]
                )

                self.get_logger().info(f'Resultado del grasp: {result}')

                if result is not None:
                    self.get_logger().info('RESULT NOT NONE')
                    self.get_logger().info(f'Pelota detectada en: {result[5]}, z={result[2]:.2f} mm')
                    # Convertir grasp a coordenadas reales (copiar lógica de RobotGrasp.grasp())
                    goal_pose = self.compute_goal_pose(result)
                    
                    # --- REEMPLAZAR LA LLAMADA DIRECTA POR ESTA VALIDACIÓN ---
                    if goal_pose is not None:
                        self.get_logger().info('GOAL NOT NONE')
                        # FASE 1 DE MOVIMIENTO XY + YAW
                        if self.GRASP_STATUS == 0:
                            # self.get_logger().info(f'Objetivo válido calculado: {goal}')
                            # Mover robot
                            self.GOAL_POS = goal_pose
                            z_segura = max(self.CURR_POS[2], 380.0)
                            approach_pose = [
                                self.GOAL_POS[0],  # X objetivo
                                self.GOAL_POS[1],  # Y objetivo
                                z_segura,          # Z alta de seguridad
                                math.radians(180.0),             # Roll forzado
                                math.radians(0.0),               # Pitch forzado
                                math.radians(self.GOAL_POS[5])   # Yaw dinámico calculado
                            ]
                            #self.set_xarm6_position_approach(approach_pose)
                            # Secuencia de grasp (bajar, cerrar, levantar, soltar)
                            #self.perform_grasp_sequence(goal_pose)
                    else:
                        self.get_logger().warn('Objetivo fuera de rango seguro o inválido algebraicamente. Ignorando movimiento.')
                
                combined = get_combined_img(color_crop, grasp_img)
                msg = self.bridge.cv2_to_imgmsg(combined, encoding='bgr8')
                self.grasp_debug_image_pub.publish(msg)

            


        

    # ----------------------------------------------------------------------
    # --- SERVICE DONE-CALLBACK FUNCTIONS ---
    # ----------------------------------------------------------------------
    def _on_xarm6_position(self, future):
        if future.result() is None:
            self.get_logger().error('Error llamando a /xarm/get_position')
            return
        self.xarm6_pose = future.result().datas
        self.get_logger().info(f'Pose XArm6 recibida: {self.xarm6_pose}')
    
    def _on_move_done(self, future):
        if future.result() is None:
            self.get_logger().error("Error ejecutando movimiento")
        else:
            self.get_logger().info("Movimiento ejecutado correctamente")


    def get_xarm6_position(self):
        # Esperar a que el servicio esté disponible
        while not self.xarm6_pos_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn('Esperando servicio /xarm/get_position...')

        req = GetFloat32List.Request()
        future = self.xarm6_pos_client.call_async(req)
        future.add_done_callback(self._on_xarm6_position)

        #rclpy.spin_until_future_complete(self, future)
        #if future.result() is None:
        #    self.get_logger().error('Error llamando a /xarm/get_position')
        #    return None
        # Guardar pose completa en la clase
        #self.xarm6_pose = future.result().datas
        # Imprimir por pantalla la pose recibida
        #self.get_logger().info(f'Pose XArm6 recibida: {self.xarm6_pose}')

    """def get_uf850_position(self):
        req = GetFloat32List.Request()
        future = self.uf850_pos_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        if future.result() is None:
            self.get_logger().error('Error llamando a /ufactory/get_position')
            return None

        # Guardar pose completa en la clase
        self.xarm6_pose = future.result().datas

        # Devolver altura del EEF (robot_pos[2])
        return self.uf850_pose[2]"""
        
    def set_xarm6_position(self, goal):
        self.get_logger().info(f'Llamando a /xarm/set_position con: {goal}')
        req = MoveCartesian.Request()
        req.pose = [float(val) for val in goal] # goal = [x, y, z, roll, pitch, yaw]
        req.speed = 70.0               
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = False

        future = self.moveit_client.call_async(req)

        future.add_done_callback(self._on_move_done)
    
    def set_xarm6_position_approach(self, goal):
        self.get_logger().info(f'Llamando a /xarm/set_position con: {goal}')
        req = MoveCartesian.Request()
        req.pose = [float(val) for val in goal] # goal = [x, y, z, roll, pitch, yaw]
        req.speed = 50.0               
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = False

        future = self.moveit_client.call_async(req)

        future.add_done_callback(self._on_move_done)

    
    def compute_goal_pose(self, result):
        return compute_goal_pose(
            result,
            self.xarm6_pose,
            self.euler_eef_to_color_opt,
            self.euler_color_to_depth_opt,
            self.gripper_z_mm,
            self.grasping_min_z,
            self.grasping_range,
            self.min_result_z
        )
    
    def perform_grasp_sequence(self, goal):
        # self.get_logger().info('Iniciando secuencia de grasping...')
        # 1. Ir al punto detectado
        self.set_xarm6_position(goal)

        # # 2. Bajar
        # down = goal.copy()
        # self.get_logger().info('Bajando el robot')
        # down[2] -= 50   # ejemplo: bajar 50 mm
        # self.set_xarm6_position(down)

        # # 3. Cerrar gripper
        # #self.close_gripper()

        # # 4. Levantar
        # lift = goal.copy()
        # lift[2] += 100
        # self.set_xarm6_position(lift)

        # # 5. Ir a RELEASE_XYZ
        # release = [self.release_x, self.release_y, self.release_z, 3.14, 0, 0]
        # self.set_xarm6_position(release)

        # # 6. Abrir gripper
        # #self.open_gripper()

        # # 7. Volver a DETECT_XYZ
        # detect = [self.detect_x, self.detect_y, self.detect_z, 3.14, 0, 0]
        # self.set_xarm6_position(detect)




"""def main(args=None):
    rclpy.init(args=args)
    node = GraspDetectorNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()"""

def main(args=None):
    rclpy.init(args=args)
    node = GraspDetectorNode()

    executor = MultiThreadedExecutor()
    executor.add_node(node)

    try:
        executor.spin()
    finally:
        node.destroy_node()
        rclpy.shutdown()



if __name__ == '__main__':
    main()