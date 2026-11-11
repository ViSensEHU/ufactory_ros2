#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

from ament_index_python.packages import get_package_share_directory

import os
import cv2
import numpy as np

from ultralytics import YOLO
import torch

import time


class SchukoDetectionNode(Node):

    def __init__(self):
        super().__init__('schuko_detection_node')

        package_share_dir = get_package_share_directory('vision_control')
        model_path = os.path.join(package_share_dir, 'model', 'yolo26-seg_finetuning.pt')
        self.model = YOLO(model_path)

        self.get_logger().info(f'CUDA available: {torch.cuda.is_available()}')
        self.get_logger().info(f'Device: {next(self.model.model.parameters()).device}')

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(Image, '/xarm6/realsense/color/image_raw', self.image_callback, 10)

        self.debug_pub = self.create_publisher(Image, '/schuko/debug_image', 10)

        self.center_pub = self.create_publisher(Point, '/schuko/center', 10)

        # --------------------------------------------------
        # Target tracking
        # --------------------------------------------------
        self.target_id = None

        self.get_logger().info('YOLO segmentation and tracking node started')

    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        except Exception as e:
            self.get_logger().error(f'CV bridge error: {e}')
            return

        debug_image = frame.copy()

        t0 = time.perf_counter()

        results = self.model.track(frame, verbose=False, persist=True, tracker="bytetrack.yaml", conf=0.25, iou=0.7, max_det=100)

        dt = time.perf_counter() - t0

        self.get_logger().info(f"Inference: {dt*1000:.1f} ms")

        boxes = results[0].boxes
        masks = results[0].masks

        # --------------------------------------------------
        # Sin detecciones
        # --------------------------------------------------
        if boxes is None or len(boxes) == 0:
            debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
            debug_msg.header = msg.header
            self.debug_pub.publish(debug_msg)
            return

        # --------------------------------------------------
        # Comprobar IDs del tracker
        # --------------------------------------------------
        if boxes.id is None:
            debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
            debug_msg.header = msg.header
            self.debug_pub.publish(debug_msg)
            return

        track_ids = boxes.id.int().cpu().tolist()

        # --------------------------------------------------
        # Seleccionar conector inicial por confianza
        # --------------------------------------------------
        if self.target_id is None:
            best_idx = max(range(len(boxes)), key=lambda i: float(boxes[i].conf[0]))
            self.target_id = track_ids[best_idx]
            self.get_logger().info(f'Target selected: ID={self.target_id}')

        # --------------------------------------------------
        # Buscar siempre el mismo ID
        # --------------------------------------------------
        target_indices = [i for i, track_id in enumerate(track_ids) if track_id == self.target_id]

        # --------------------------------------------------
        # Dibujar todas las detecciones con sus IDs
        # --------------------------------------------------
        for i, box in enumerate(boxes):

            x1, y1, x2, y2 = box.xyxy[0].cpu().numpy()
            confidence = float(box.conf[0])
            cls_id = int(box.cls[0])
            label = self.model.names[cls_id]
            track_id = track_ids[i]

            color = (0, 255, 0) if track_id == self.target_id else (255, 0, 0)

            cv2.rectangle(debug_image, (int(x1), int(y1)), (int(x2), int(y2)), color, 2)

            cv2.putText(debug_image, f'ID: {track_id} {label} {confidence:.2f}', (int(x1), int(y1) - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.6, color, 2)

        # --------------------------------------------------
        # Procesar únicamente el conector objetivo
        # --------------------------------------------------
        if not target_indices:

            self.get_logger().warn(f'Target ID={self.target_id} temporarily lost')

        else:

            best_idx = target_indices[0]
            best_box = boxes[best_idx]

            x1, y1, x2, y2 = best_box.xyxy[0].cpu().numpy()
            confidence = float(best_box.conf[0])

            cx = (x1 + x2) / 2.0
            cy = (y1 + y2) / 2.0

            # --------------------------------------------------
            # Dibujar máscara del objetivo
            # --------------------------------------------------
            if masks is not None:

                mask = masks.data[best_idx].cpu().numpy()
                mask = cv2.resize(mask, (frame.shape[1], frame.shape[0]), interpolation=cv2.INTER_NEAREST)
                mask = mask > 0.5

                overlay = debug_image.copy()
                overlay[mask] = (0, 255, 0)
                debug_image = cv2.addWeighted(debug_image, 0.6, overlay, 0.4, 0)

            # --------------------------------------------------
            # Publicar centro del objetivo
            # --------------------------------------------------
            center_msg = Point()
            center_msg.x = float(cx)
            center_msg.y = float(cy)
            center_msg.z = float(confidence)

            self.center_pub.publish(center_msg)

            # --------------------------------------------------
            # Dibujar centro
            # --------------------------------------------------
            cv2.circle(debug_image, (int(cx), int(cy)), 5, (0, 0, 255), -1)

            self.get_logger().info(f'TARGET ID={self.target_id}: center=({cx:.1f}, {cy:.1f}) conf={confidence:.2f}')

        # --------------------------------------------------
        # Publicar imagen debug
        # --------------------------------------------------
        debug_msg = self.bridge.cv2_to_imgmsg(debug_image, encoding='bgr8')
        debug_msg.header = msg.header

        self.debug_pub.publish(debug_msg)


def main(args=None):

    rclpy.init(args=args)
    node = SchukoDetectionNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()
