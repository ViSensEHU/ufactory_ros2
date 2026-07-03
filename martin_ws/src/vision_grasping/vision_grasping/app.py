import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from sensor_msgs.msg import Image, CameraInfo
from xarm_msgs.srv import MoveCartesian
from xarm_msgs.srv import GetFloat32List

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
from .cv_grasp_detector import CVGraspDetector
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
        self.xarm6_pose = None
        self.uf850_pose = None

        # --- Colas internas del detector ---
        self.depth_img_que = Queue(1)
        self.ggcnn_cmd_que = Queue(1)

        # --- Estado ---
        self.depth_camera_k = None
        self.detector_initialized = False
        self.grasp_detector = None

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
        
        # Intrinsecas del depth (profundidad)
        self.create_subscription(
            CameraInfo,
            '/camera/camera/depth/camera_info',
            self.depth_camera_info_callback,
            10,
            callback_group=self.cb_group
        )

        # Imagen de depth (profundidad)
        self.create_subscription(
            Image,
            '/camera/camera/depth/image_rect_raw',
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
        while not self.moveit_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().warn("Esperando servicio /xarm/set_position...")



    # ----------------------------------------------------------------------
    # --- CALLBACKS ---
    # ----------------------------------------------------------------------

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
        if self.color_image is None or self.depth_image is None:
            return
        if self.crop_size is None:
            return

        self.get_logger().info('process_frame ejecutado')

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
        self.get_xarm6_position()

        if self.xarm6_pose is not None:
            # Identificación y reconocimiento de la pelota
            grasp_img, result = self.grasp_detector.get_grasp_img(
                depth_crop,
                self.depth_camera_k_crop,
                self.xarm6_pose[2]
            )

            if result is not None:
                # Convertir grasp a coordenadas reales (copiar lógica de RobotGrasp.grasp())
                goal = self.compute_goal_pose(result)
                # Mover robot
                #self.set_xarm6_position(goal)
                # Secuencia de grasp (bajar, cerrar, levantar, soltar)
                self.perform_grasp_sequence(goal)
            
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
        req = MoveCartesian.Request()
        req.pose = goal              # goal = [x, y, z, roll, pitch, yaw]
        req.speed = 50               # ajusta según tu robot
        req.acc = 500
        req.mvtime = 0
        req.wait = True

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
        # 1. Ir al punto detectado
        self.set_xarm6_position(goal)

        # 2. Bajar
        down = goal.copy()
        down[2] -= 50   # ejemplo: bajar 50 mm
        self.set_xarm6_position(down)

        # 3. Cerrar gripper
        #self.close_gripper()

        # 4. Levantar
        lift = goal.copy()
        lift[2] += 100
        self.set_xarm6_position(lift)

        # 5. Ir a RELEASE_XYZ
        release = [self.release_x, self.release_y, self.release_z, 3.14, 0, 0]
        self.set_xarm6_position(release)

        # 6. Abrir gripper
        #self.open_gripper()

        # 7. Volver a DETECT_XYZ
        detect = [self.detect_x, self.detect_y, self.detect_z, 3.14, 0, 0]
        self.set_xarm6_position(detect)




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
