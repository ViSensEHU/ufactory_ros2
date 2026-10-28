"""#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

from xarm_msgs.srv import MoveCartesian


class CenterVisualServoing(Node):

    def __init__(self):

        super().__init__('center_visual_servoing')

        # -----------------------------
        # Cliente MoveCartesian
        # -----------------------------

        self.move_client = self.create_client(
            MoveCartesian,
            '/xarm/set_position'
        )

        while not self.move_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Esperando a /xarm/set_position...'
            )

        self.get_logger().info(
            'Servicio MoveCartesian disponible.'
        )

        # -----------------------------
        # Posición actual objetivo
        # -----------------------------

        self.pose = [
            300.0,      # X [mm]
            0.0,        # Y [mm]
            400.0,      # Z [mm]
            math.pi,    # Roll
            0.0,        # Pitch
            0.0         # Yaw
        ]

        # -----------------------------
        # Cámara
        # -----------------------------

        self.image_width = 640
        self.image_height = 480

        self.cx = self.image_width / 2.0
        self.cy = self.image_height / 2.0

        # -----------------------------
        # Control
        # -----------------------------

        self.deadband_px = 20

        # mm por píxel
        self.kx = 0.20
        self.ky = 0.20

        self.max_step_mm = 10.0

        self.command_in_progress = False

        # -----------------------------
        # Subscriber
        # -----------------------------

        self.ball_sub = self.create_subscription(
            Point,
            '/green_ball/center',
            self.ball_callback,
            10
        )

        self.get_logger().info(
            'Center visual servoing iniciado.'
        )

    # --------------------------------------------------
    # Callback detección
    # --------------------------------------------------

    def ball_callback(self, msg):

        if self.command_in_progress:
            return

        u = float(msg.x)
        v = float(msg.y)

        error_u = u - self.cx
        error_v = v - self.cy

        self.get_logger().info(
            f'Ball: ({u:.1f}, {v:.1f}) | '
            f'Error: ({error_u:.1f}, {error_v:.1f})'
        )

        if (
            abs(error_u) < self.deadband_px
            and
            abs(error_v) < self.deadband_px
        ):
            return

        #
        # IMPORTANTE:
        #
        # Los signos probablemente haya que invertirlos
        # según cómo esté montada la cámara.
        #
        # Primera prueba:
        #

        delta_x = -self.ky * error_v
        delta_y = -self.kx * error_u

        delta_x = max(
            -self.max_step_mm,
            min(self.max_step_mm, delta_x)
        )

        delta_y = max(
            -self.max_step_mm,
            min(self.max_step_mm, delta_y)
        )

        self.pose[0] += delta_x
        self.pose[1] += delta_y

        self.get_logger().info(
            f'Corrección -> '
            f'dX={delta_x:.2f} mm, '
            f'dY={delta_y:.2f} mm'
        )

        self.send_position()

    # --------------------------------------------------
    # Enviar pose
    # --------------------------------------------------

    def send_position(self):

        req = MoveCartesian.Request()

        req.pose = [
            float(value)
            for value in self.pose
        ]

        req.speed = 50.0
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = False

        self.command_in_progress = True

        future = self.move_client.call_async(req)

        future.add_done_callback(
            self.movement_callback
        )

    # --------------------------------------------------
    # Callback respuesta servicio
    # --------------------------------------------------

    def movement_callback(self, future):

        self.command_in_progress = False

        try:

            response = future.result()

            if response is None:

                self.get_logger().error(
                    'Respuesta vacía.'
                )

                return

            self.get_logger().info(
                f'Nueva pose: '
                f'X={self.pose[0]:.1f} '
                f'Y={self.pose[1]:.1f}'
            )

        except Exception as e:

            self.get_logger().error(
                f'Error: {e}'
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
    main()"""

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