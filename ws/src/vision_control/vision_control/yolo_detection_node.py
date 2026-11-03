#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ament_index_python.packages import get_package_share_directory

import os

import cv2
# import numpy as np

from ultralytics import YOLO
import torch

import time


class YoloDetectionNode(Node):

    def __init__(self):
        super().__init__('yolo_detection_node')

        package_share_dir = get_package_share_directory('vision_control')
        model_path = os.path.join(package_share_dir, 'model', 'yolo11n.pt')
        self.model = YOLO(model_path)

        self.get_logger().info(
            f'CUDA available: {torch.cuda.is_available()}'
        )

        self.get_logger().info(
            f'Device: {next(self.model.model.parameters()).device}'
        )

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            '/xarm6/realsense/color/image_raw',
            self.image_callback,
            10
        )

        self.debug_pub = self.create_publisher(
            Image,
            '/green_ball/debug_image',
            10
        )

        self.center_pub = self.create_publisher(
            Point,
            '/green_ball/center',
            10
        )

        self.get_logger().info('Green filter node started')

    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        except Exception as e:
            self.get_logger().error(f'CV bridge error: {e}')
            return

        debug_image = frame.copy()

        t0 = time.perf_counter()

        results = self.model(
            frame,
            verbose=False
        )

        dt = time.perf_counter() - t0

        self.get_logger().info(
            f"Inference: {dt*1000:.1f} ms"
        )

        results = self.model(frame, verbose=False)
        boxes = results[0].boxes

        # --------------------------------------------------
        # Sin detecciones
        # --------------------------------------------------
        if len(boxes) == 0:
            debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
            debug_msg.header = msg.header
            self.debug_pub.publish(debug_msg)

            return

        # --------------------------------------------------
        # Seleccionar detección con mayor confianza
        # --------------------------------------------------
        best_box = max(boxes, key=lambda b: float(b.conf[0]))

        x1, y1, x2, y2 = best_box.xyxy[0].cpu().numpy()
        confidence = float(best_box.conf[0])
        cls_id = int(best_box.cls[0])
        label = self.model.names[cls_id]

        # --------------------------------------------------
        # Centro de la bounding box
        # --------------------------------------------------
        cx = (x1 + x2) / 2.0
        cy = (y1 + y2) / 2.0

        # --------------------------------------------------
        # Publicar centro
        # --------------------------------------------------
        center_msg = Point()

        center_msg.x = float(cx)
        center_msg.y = float(cy)
        center_msg.z = float(confidence)

        self.center_pub.publish(center_msg)

        # --------------------------------------------------
        # Dibujar bounding box
        # --------------------------------------------------
        cv2.rectangle(debug_image, (int(x1), int(y1)), (int(x2), int(y2)), (0, 255, 0), 2)

        # --------------------------------------------------
        # Dibujar centro
        # --------------------------------------------------
        cv2.circle(debug_image, (int(cx), int(cy)), 5, (0, 0, 255), -1)

        # --------------------------------------------------
        # Etiqueta
        # --------------------------------------------------
        cv2.putText(debug_image, f'{label} {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)

        self.get_logger().info(
            f'Detected {label}: '
            f'center=({cx:.1f}, {cy:.1f}) '
            f'conf={confidence:.2f}'
        )

        # --------------------------------------------------
        # Publicar imagen debug
        # --------------------------------------------------
        debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
        debug_msg.header = msg.header

        self.debug_pub.publish(debug_msg)


def main(args=None):

    rclpy.init(args=args)
    node = YoloDetectionNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()