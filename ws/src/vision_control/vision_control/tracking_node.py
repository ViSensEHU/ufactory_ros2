#!/usr/bin/env python3

import math

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point
from std_msgs.msg import String
from std_srvs.srv import Trigger

from xarm_msgs.srv import MoveCartesian, SetInt16, SetInt16ById, GripperMove, SetFloat32



class TrackingNode(Node):

    def __init__(self):
        super().__init__('tracking_node')

        # --------------------------------------------------
        # Estado interno
        # --------------------------------------------------
        self.active = False
        self.initialized = False
        self.command_in_progress = False
        self.finish_requested = False
        self.init_step = 0

        # --------------------------------------------------
        # Clientes del xArm
        # --------------------------------------------------
        self.motion_enable_client = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.mode_client = self.create_client(SetInt16, '/xarm/set_mode')
        self.state_client = self.create_client(SetInt16, '/xarm/set_state')
        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position')
        self.gripper_enable_client = self.create_client(SetInt16, '/xarm/set_gripper_enable')
        self.gripper_mode_client = self.create_client(SetInt16, '/xarm/set_gripper_mode')
        self.gripper_speed_client = self.create_client(SetFloat32, '/xarm/set_gripper_speed')
        self.gripper_client = self.create_client(GripperMove, '/xarm/set_gripper_position')

        # --------------------------------------------------
        # Comunicación con la FSM
        # --------------------------------------------------
        self.transition_pub = self.create_publisher(String, '/fsm/transition', 10)
        self.finish_srv = self.create_service(Trigger, '/tracking/finish', self.finish_callback)

        # --------------------------------------------------
        # Error visual
        # --------------------------------------------------
        self.error_sub = self.create_subscription(Point, '/green_ball/error', self.error_callback, 10)

        # --------------------------------------------------
        # Pose inicial [mm, rad]
        # --------------------------------------------------
        self.pose = [300.0, 0.0, 400.0, math.pi, 0.0, 0.0]

        # --------------------------------------------------
        # Parámetros de control
        # --------------------------------------------------
        self.deadband_px = 20.0
        self.kx = 0.02
        self.ky = 0.02
        self.max_step_mm = 1.0

        self.get_logger().info('TrackingNode iniciado. Preparando el xArm.')

        # --------------------------------------------------
        # Comprobar disponibilidad de servicios
        # --------------------------------------------------
        self.xarm_clients = [
            self.motion_enable_client,
            self.mode_client,
            self.state_client,
            self.move_client,
            self.gripper_enable_client,
            self.gripper_mode_client,
            self.gripper_speed_client,
            self.gripper_client
        ]

        self.wait_timer = self.create_timer(1.0, self.check_services)

    # ==================================================
    # INICIALIZACIÓN
    # ==================================================

    def check_services(self):
        if self.initialized or self.command_in_progress:
            return

        if not all(client.service_is_ready() for client in self.xarm_clients):
            self.get_logger().info('Esperando a los servicios del xArm...')
            return

        self.wait_timer.cancel()
        self.init_step = 0
        self.execute_init_step()

    def execute_init_step(self):
        if self.command_in_progress:
            return

        steps = [
            ('Habilitar movimiento', self.motion_enable_client, self.motion_enable_request()),
            ('Configurar modo 0', self.mode_client, self.mode_request(0)),
            ('Configurar estado 0', self.state_client, self.state_request(0)),
            ('Habilitar pinza', self.gripper_enable_client, self.gripper_enable_request()),
            ('Configurar modo de pinza 0', self.gripper_mode_client, self.gripper_mode_request(0)),
            ('Configurar velocidad de pinza 1500', self.gripper_speed_client, self.gripper_speed_request(1500.0)),
            ('Abrir pinza a 700', self.gripper_client, self.gripper_position_request(700.0)),
            ('Mover a pose inicial', self.move_client, self.initial_pose_request()),
            ('Configurar modo 7', self.mode_client, self.mode_request(7)),
            ('Configurar estado 0', self.state_client, self.state_request(0)),
        ]


        if self.init_step >= len(steps):
            self.initialized = True
            self.active = True
            self.get_logger().info('xArm preparado. Tracking activado.')
            return

        label, client, request = steps[self.init_step]

        self.get_logger().info(f'Inicialización: {label}')

        self.command_in_progress = True
        future = client.call_async(request)
        future.add_done_callback(lambda f: self.init_callback(f, label))

    def init_callback(self, future, label):
        self.command_in_progress = False

        try:
            response = future.result()

            if response is None:
                self.get_logger().error(f'{label}: no se recibió respuesta.')
                self.initialization_failed()
                return

            ret = getattr(response, 'ret', 0)

            if ret != 0:
                self.get_logger().error(f'{label}: error del xArm, ret={ret}.')
                self.initialization_failed()
                return

            self.get_logger().info(f'{label}: completado.')

            self.init_step += 1
            self.execute_init_step()

        except Exception as e:
            self.get_logger().error(f'Error durante {label}: {e}')
            self.initialization_failed()

    def initialization_failed(self):
        self.active = False
        self.initialized = False
        self.get_logger().error('Falló la inicialización. Tracking no iniciado.')

    # ==================================================
    # PETICIONES DEL XARM
    # ==================================================
    def gripper_enable_request(self):
        req = SetInt16.Request()
        req.data = 1
        return req

    def gripper_mode_request(self, mode):
        req = SetInt16.Request()
        req.data = int(mode)
        return req

    def gripper_speed_request(self, speed):
        req = SetFloat32.Request()
        req.data = float(speed)
        return req

    def gripper_position_request(self, position):
        req = GripperMove.Request()
        req.pos = float(position)
        return req
    
    def motion_enable_request(self):
        req = SetInt16ById.Request()
        req.id = 8
        req.data = 1
        return req

    def mode_request(self, mode):
        req = SetInt16.Request()
        req.data = int(mode)
        return req

    def state_request(self, state):
        req = SetInt16.Request()
        req.data = int(state)
        return req

    def initial_pose_request(self):
        req = MoveCartesian.Request()
        req.pose = [float(v) for v in self.pose]
        req.speed = 50.0
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = True
        return req

    # ==================================================
    # CALLBACK ERROR VISUAL
    # ==================================================

    def error_callback(self, msg):
        if not self.active or self.finish_requested or self.command_in_progress:
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

        # Izquierda imagen -> Y+
        # Derecha imagen   -> Y-
        # Arriba imagen    -> X+
        # Abajo imagen     -> X-

        delta_x = max(-self.max_step_mm, min(self.max_step_mm, -self.kx * error_v))
        delta_y = max(-self.max_step_mm, min(self.max_step_mm, -self.ky * error_u))

        self.pose[0] += delta_x
        self.pose[1] += delta_y

        self.get_logger().info(
            f'Error=({error_u:.1f},{error_v:.1f}) px | '
            f'R={radius:.1f} px | '
            f'dX={delta_x:.2f} mm | '
            f'dY={delta_y:.2f} mm'
        )

        self.send_position()

    # ==================================================
    # ENVIAR POSICIÓN
    # ==================================================

    def send_position(self):
        if not self.move_client.service_is_ready():
            self.get_logger().warning('Servicio /xarm/set_position no disponible.')
            return

        req = MoveCartesian.Request()
        req.pose = [float(v) for v in self.pose]
        req.speed = 50.0
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = False

        self.command_in_progress = True
        future = self.move_client.call_async(req)
        future.add_done_callback(self.movement_callback)

    # ==================================================
    # RESPUESTA DE MOVIMIENTO
    # ==================================================

    def movement_callback(self, future):
        self.command_in_progress = False

        try:
            response = future.result()

            if response is None:
                self.get_logger().error('El servicio no devolvió respuesta.')
                return

            ret = getattr(response, 'ret', 0)

            if ret != 0:
                self.get_logger().error(f'El xArm ha rechazado el movimiento: ret={ret}.')
                return

            self.get_logger().info(
                f'Pose objetivo -> X={self.pose[0]:.1f} mm, '
                f'Y={self.pose[1]:.1f} mm'
            )

            if self.finish_requested:
                self.publish_transition()

        except Exception as e:
            self.get_logger().error(f'Error ejecutando movimiento: {e}')

    # ==================================================
    # FINALIZACIÓN SOLICITADA POR LA FSM
    # ==================================================

    def finish_callback(self, request, response):
        if not self.initialized:
            response.success = False
            response.message = 'El tracking todavía no está inicializado.'
            return response

        if self.finish_requested:
            response.success = True
            response.message = 'La finalización del tracking ya ha sido solicitada.'
            return response

        self.finish_requested = True
        self.active = False

        self.get_logger().info('Finalización del tracking solicitada.')

        if not self.command_in_progress:
            self.publish_transition()

        response.success = True
        response.message = 'Tracking detenido; se notificará la transición cuando corresponda.'
        return response

    def publish_transition(self):
        if not self.finish_requested:
            return

        msg = String()
        msg.data = 'TRACKING_COMPLETE'
        self.transition_pub.publish(msg)

        self.get_logger().info('Evento publicado: TRACKING_COMPLETE')

    # ==================================================
    # MAIN
    # ==================================================


def main(args=None):
    rclpy.init(args=args)
    node = TrackingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
