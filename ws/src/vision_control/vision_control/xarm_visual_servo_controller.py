#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

from xarm_msgs.srv import MoveCartesian


class XArmVisualServoController(Node):

    def __init__(self):

        super().__init__('xarm_visual_servo_controller')

        # --------------------------------------------------
        # Cliente MoveCartesian
        # --------------------------------------------------

        self.move_client = self.create_client(
            MoveCartesian,
            '/xarm/set_position'
        )

        while not self.move_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                'Esperando al servicio /xarm/set_position...'
            )

        self.get_logger().info(
            'Servicio /xarm/set_position disponible.'
        )

        # --------------------------------------------------
        # Pose inicial
        # --------------------------------------------------

        self.pose = [
            300.0,     # X [mm]
            0.0,       # Y [mm]
            400.0,     # Z [mm]
            math.pi,   # Roll
            0.0,       # Pitch
            0.0        # Yaw
        ]

        # --------------------------------------------------
        # Parámetros de control
        # --------------------------------------------------

        self.deadband_px = 20

        # Ganancias [mm/px]
        self.kx = 0.02
        self.ky = 0.02

        # Corrección máxima por iteración
        self.max_step_mm = 1.0

        self.command_in_progress = False

        # --------------------------------------------------
        # Subscriber
        # --------------------------------------------------

        self.error_sub = self.create_subscription(
            Point,
            '/green_ball/error',
            self.error_callback,
            10
        )

        self.get_logger().info(
            'XArm Visual Servo Controller iniciado.'
        )

    # --------------------------------------------------
    # Callback error visual
    # --------------------------------------------------

    def error_callback(self, msg):

        if self.command_in_progress:
            return

        error_u = float(msg.x)
        error_v = float(msg.y)
        radius = float(msg.z)

        if abs(error_u) < self.deadband_px:
            error_u = 0.0

        if abs(error_v) < self.deadband_px:
            error_v = 0.0

        if error_u == 0.0 and error_v == 0.0:
            return

        #
        # Mapeo experimental:
        #
        # Izquierda imagen -> Y+
        # Derecha imagen   -> Y-
        #
        # Arriba imagen    -> X+
        # Abajo imagen     -> X-
        #

        delta_x = -self.kx * error_v
        delta_y = -self.ky * error_u

        # Saturación

        delta_x = max(
            -self.max_step_mm,
            min(self.max_step_mm, delta_x)
        )

        delta_y = max(
            -self.max_step_mm,
            min(self.max_step_mm, delta_y)
        )

        # Actualizar pose objetivo

        self.pose[0] += delta_x
        self.pose[1] += delta_y

        self.get_logger().info(
            f'Error=({error_u:.1f},{error_v:.1f}) px | '
            f'R={radius:.1f} px | '
            f'dX={delta_x:.2f} mm | '
            f'dY={delta_y:.2f} mm'
        )

        self.send_position()

    # --------------------------------------------------
    # Enviar posición
    # --------------------------------------------------

    def send_position(self):

        req = MoveCartesian.Request()

        req.pose = [
            float(v)
            for v in self.pose
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
    # Respuesta servicio
    # --------------------------------------------------

    def movement_callback(self, future):

        self.command_in_progress = False

        try:

            response = future.result()

            if response is None:

                self.get_logger().error(
                    'El servicio no devolvió respuesta.'
                )

                return

            self.get_logger().info(
                f'Pose objetivo -> '
                f'X={self.pose[0]:.1f} mm, '
                f'Y={self.pose[1]:.1f} mm'
            )

        except Exception as e:

            self.get_logger().error(
                f'Error ejecutando movimiento: {e}'
            )


def main(args=None):

    rclpy.init(args=args)

    node = XArmVisualServoController()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass

    node.destroy_node()

    rclpy.shutdown()


if __name__ == '__main__':
    main()