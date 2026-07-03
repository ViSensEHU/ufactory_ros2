import rclpy
from rclpy.node import Node
from rclpy.callback_groups import ReentrantCallbackGroup
from rclpy.executors import MultiThreadedExecutor

from sensor_msgs.msg import Image, CameraInfo

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
from .utils import compute_crop_and_intrinsics

class GraspDetectorNode(Node):
    def __init__(self):
        super().__init__('grasp_detector_node')

        self.get_logger().info('Nodo vision_grasping iniciado.')

        self.cb_group = ReentrantCallbackGroup()

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

        # Aquí más adelante llamaremos a get_grasp_img()


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
