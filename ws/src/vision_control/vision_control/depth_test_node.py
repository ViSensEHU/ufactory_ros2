#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from sensor_msgs.msg import Image
from cv_bridge import CvBridge

import numpy as np


class BallDepthNode(Node):

    def __init__(self):

        super().__init__('ball_depth_node')

        self.bridge = CvBridge()

        self.ball_u = None
        self.ball_v = None
        self.ball_radius = None

        self.center_sub = self.create_subscription(
            Point,
            '/green_ball/center',
            self.center_callback,
            10
        )

        self.depth_sub = self.create_subscription(
            Image,
            '/xarm6/realsense/aligned_depth_to_color/image_raw',
            self.depth_callback,
            10
        )

        self.get_logger().info(
            'BallDepthNode iniciado. Esperando centro de pelota.'
        )

    def center_callback(self, msg):

        self.ball_u = int(msg.x)
        self.ball_v = int(msg.y)
        self.ball_radius = msg.z

    def depth_callback(self, msg):

        if self.ball_u is None:
            return

        try:

            depth_image = self.bridge.imgmsg_to_cv2(
                msg,
                desired_encoding='passthrough'
            )

        except Exception as e:

            self.get_logger().error(
                f'Error convirtiendo imagen depth: {e}'
            )
            return

        height, width = depth_image.shape

        if (
            self.ball_u < 0 or self.ball_u >= width or
            self.ball_v < 0 or self.ball_v >= height
        ):
            return

        depth_center = depth_image[
            self.ball_v,
            self.ball_u
        ]

        window_size = 2

        u_min = max(0, self.ball_u - window_size)
        u_max = min(width, self.ball_u + window_size + 1)

        v_min = max(0, self.ball_v - window_size)
        v_max = min(height, self.ball_v + window_size + 1)

        roi = depth_image[
            v_min:v_max,
            u_min:u_max
        ]

        valid_depths = roi[roi > 0]

        if len(valid_depths) == 0:

            self.get_logger().warn(
                f'Sin profundidad válida en ({self.ball_u}, {self.ball_v})'
            )
            return

        depth_mean = float(np.mean(valid_depths))

        self.get_logger().info(
            f'Centro=({self.ball_u}, {self.ball_v}) | '
            f'Radio={self.ball_radius:.1f}px | '
            f'Depth pixel={depth_center} mm | '
            f'Depth media={depth_mean:.1f} mm '
            f'({depth_mean/1000.0:.3f} m)'
        )


def main(args=None):

    rclpy.init(args=args)

    node = BallDepthNode()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()