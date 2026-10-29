#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point


class CenterVisualServoing(Node):

    def __init__(self):

        super().__init__('center_visual_servoing')

        # Centro de la imagen
        self.image_width = 640
        self.image_height = 480

        # Centro de la pinza (traslación cámara)
        self.u_ref = 360.0
        self.v_ref = 382.0

        """self.cx = self.image_width / 2.0
        self.cy = self.image_height / 2.0"""

        # Zona muerta
        self.deadband_px = 20

        # Subscriber
        self.center_sub = self.create_subscription(
            Point,
            '/green_ball/center',
            self.ball_callback,
            10
        )

        # Publisher
        self.error_pub = self.create_publisher(
            Point,
            '/green_ball/error',
            10
        )

        self.get_logger().info(
            'Center visual servoing node started.'
        )

    def ball_callback(self, msg):

        u = float(msg.x)
        v = float(msg.y)
        radius = float(msg.z)

        error_u = u - self.u_ref #self.cx
        error_v = v - self.v_ref #self.cy

        self.get_logger().info("REFS")

        # Zona muerta
        if abs(error_u) < self.deadband_px:
            error_u = 0.0

        if abs(error_v) < self.deadband_px:
            error_v = 0.0

        error_msg = Point()

        error_msg.x = float(error_u)
        error_msg.y = float(error_v)
        error_msg.z = float(radius)

        self.error_pub.publish(error_msg)

        self.get_logger().info(
            f'Ball=({u:.0f},{v:.0f}) '
            f'Error=({error_u:.0f},{error_v:.0f}) '
            f'Radius={radius:.1f}'
        )


def main(args=None):

    rclpy.init(args=args)

    node = CenterVisualServoing()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()