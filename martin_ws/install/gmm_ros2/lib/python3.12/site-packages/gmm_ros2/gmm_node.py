import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class GMMNode(Node):

    def __init__(self):

        super().__init__('gmm_node')

        # -----------------------------
        # Parámetros
        # -----------------------------

        self.history = 200
        self.var_threshold = 25
        self.warmup_frames = 120

        self.frame_count = 0
        self.background_ready = False


        # -----------------------------
        # ROS interfaces
        # -----------------------------

        self.bridge = CvBridge()


        self.image_sub = self.create_subscription(
            Image,
            '/camera/camera/color/image_raw',
            self.image_callback,
            10
        )


        self.foreground_pub = self.create_publisher(
            Image,
            '/camera/gmm/foreground_image',
            10
        )


        self.mask_pub = self.create_publisher(
            Image,
            '/camera/gmm/mask',
            10
        )


        # -----------------------------
        # Modelo GMM / MOG2
        # -----------------------------

        self.mog2 = cv2.createBackgroundSubtractorMOG2(
            history=self.history,
            varThreshold=self.var_threshold,
            detectShadows=False
        )


        self.get_logger().info(
            "GMM node iniciado. Aprendiendo fondo..."
        )


    def image_callback(self, msg):

        # ROS Image -> OpenCV

        frame = self.bridge.imgmsg_to_cv2(
            msg,
            desired_encoding='bgr8'
        )


        # Aplicar modelo

        raw_mask = self.mog2.apply(frame)


        self.frame_count += 1


        # -----------------------------
        # Fase aprendizaje fondo
        # -----------------------------

        if self.frame_count < self.warmup_frames:

            mask = np.zeros(
                frame.shape[:2],
                dtype=np.uint8
            )

            foreground = np.zeros_like(frame)


        else:

            if not self.background_ready:

                self.background_ready = True

                self.get_logger().info(
                    "Fondo aprendido. Iniciando deteccion de foreground."
                )


            # -------------------------
            # Procesado máscara
            # -------------------------

            _, mask = cv2.threshold(
                raw_mask,
                200,
                255,
                cv2.THRESH_BINARY
            )


            # Eliminación de ruido

            kernel = cv2.getStructuringElement(
                cv2.MORPH_ELLIPSE,
                (5, 5)
            )


            mask = cv2.morphologyEx(
                mask,
                cv2.MORPH_OPEN,
                kernel
            )


            # Rellenar pequeñas zonas

            mask = cv2.dilate(
                mask,
                kernel,
                iterations=2
            )


            # -------------------------
            # Aplicar máscara al RGB
            # -------------------------

            foreground = cv2.bitwise_and(
                frame,
                frame,
                mask=mask
            )


        # -----------------------------
        # Publicar imagen foreground
        # -----------------------------

        foreground_msg = self.bridge.cv2_to_imgmsg(
            foreground,
            encoding='bgr8'
        )

        foreground_msg.header = msg.header

        self.foreground_pub.publish(
            foreground_msg
        )


        # -----------------------------
        # Publicar máscara
        # -----------------------------

        mask_msg = self.bridge.cv2_to_imgmsg(
            mask,
            encoding='mono8'
        )

        mask_msg.header = msg.header

        self.mask_pub.publish(
            mask_msg
        )


def main(args=None):

    rclpy.init(args=args)

    node = GMMNode()

    rclpy.spin(node)

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()