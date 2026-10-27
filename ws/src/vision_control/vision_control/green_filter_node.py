#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import cv2
import numpy as np


class GreenFilterNode(Node):

    def __init__(self):
        super().__init__('green_filter_node')

        self.bridge = CvBridge()

        self.image_sub = self.create_subscription(
            Image,
            '/xarm6/realsense/color/image_raw',
            self.image_callback,
            10
        )

        self.mask_pub = self.create_publisher(
            Image,
            '/green_ball/mask',
            10
        )

        self.debug_pub = self.create_publisher(
            Image,
            '/green_ball/debug_image',
            10
        )

        self.get_logger().info('Green filter node started')

    def image_callback(self, msg):

        try:
            frame = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        except Exception as e:
            self.get_logger().error(f'CV bridge error: {e}')
            return

        # BGR -> HSV
        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        # Green thresholds
        lower_green = np.array([35, 80, 50])
        upper_green = np.array([85, 255, 255])

        mask = cv2.inRange(
            hsv,
            lower_green,
            upper_green
        )

        # Morphological filtering
        kernel = np.ones((5, 5), np.uint8)

        mask = cv2.erode(mask, kernel, iterations=1)
        mask = cv2.dilate(mask, kernel, iterations=2)

        debug_image = frame.copy()

        contours, _ = cv2.findContours(
            mask,
            cv2.RETR_EXTERNAL,
            cv2.CHAIN_APPROX_SIMPLE
        )

        if len(contours) > 0:

            largest_contour = max(
                contours,
                key=cv2.contourArea
            )

            area = cv2.contourArea(largest_contour)

            if area > 300:

                (x, y), radius = cv2.minEnclosingCircle(
                    largest_contour
                )

                center = (int(x), int(y))

                cv2.circle(
                    debug_image,
                    center,
                    int(radius),
                    (0, 0, 255),
                    3
                )

                cv2.circle(
                    debug_image,
                    center,
                    5,
                    (255, 0, 0),
                    -1
                )

                cv2.putText(
                    debug_image,
                    f'({int(x)}, {int(y)})',
                    (int(x) + 10, int(y) - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6,
                    (0, 255, 0),
                    2
                )

        # Publish mask
        mask_msg = self.bridge.cv2_to_imgmsg(
            mask,
            encoding='mono8'
        )

        mask_msg.header = msg.header

        self.mask_pub.publish(mask_msg)

        # Publish debug image
        debug_msg = self.bridge.cv2_to_imgmsg(
            debug_image,
            encoding='bgr8'
        )

        debug_msg.header = msg.header

        self.debug_pub.publish(debug_msg)


def main(args=None):

    rclpy.init(args=args)

    node = GreenFilterNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()