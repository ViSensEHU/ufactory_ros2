#!/usr/bin/env python3

import rclpy
from rclpy.node import Node

from std_msgs.msg import String
from std_srvs.srv import Trigger

from xarm_msgs.srv import MoveCartesian, GripperMove, SetInt16, SetInt16ById, SetFloat32


class GraspingNode(Node):

    def __init__(self):
        super().__init__('grasping_node')

        # --------------------------------------------------
        # Estado del nodo
        # --------------------------------------------------
        self.active = False
        self.command_in_progress = False
        self.current_step = 0

        # --------------------------------------------------
        # Clientes del xArm
        # --------------------------------------------------
        self.motion_enable_client = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.mode_client = self.create_client(SetInt16, '/xarm/set_mode')
        self.state_client = self.create_client(SetInt16, '/xarm/set_state')

        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position_aa')

        self.gripper_enable_client = self.create_client(SetInt16, '/xarm/set_gripper_enable')
        self.gripper_mode_client = self.create_client(SetInt16, '/xarm/set_gripper_mode')
        self.gripper_speed_client = self.create_client(SetFloat32, '/xarm/set_gripper_speed')
        self.gripper_client = self.create_client(GripperMove, '/xarm/set_gripper_position')

        # --------------------------------------------------
        # Comunicación con la FSM
        # --------------------------------------------------
        self.transition_pub = self.create_publisher(String, '/fsm/transition', 10)
        self.start_srv = self.create_service(Trigger, '/grasping/start', self.start_callback)

        self.get_logger().info('GraspingNode iniciado. Esperando orden de la FSM.')

    # ==================================================
    # INICIAR GRASPING
    # ==================================================

    def start_callback(self, request, response):
        if self.active:
            response.success = False
            response.message = 'El grasping ya está en ejecución.'
            return response

        self.active = True
        self.current_step = 0

        self.get_logger().info('Iniciando secuencia de grasping.')

        self.execute_next_step()

        response.success = True
        response.message = 'Secuencia de grasping iniciada.'
        return response

    # ==================================================
    # SECUENCIA DE OPERACIONES
    # ==================================================

    def execute_next_step(self):
        if not self.active or self.command_in_progress:
            return

        steps = [
            ('Habilitar movimiento', self.motion_enable_client, self.motion_enable_request()),
            ('Configurar modo del xArm', self.mode_client, self.mode_request(0)),
            ('Preparar estado del xArm', self.state_client, self.state_request(0)),
            ('Habilitar pinza', self.gripper_enable_client, self.int16_request(1)),
            ('Configurar modo de pinza', self.gripper_mode_client, self.int16_request(0)),
            ('Configurar velocidad de pinza', self.gripper_speed_client, self.float_request(1500.0)),
            ('Bajar 205 mm', self.move_client, self.relative_z_request(-220.0)),
            ('Cerrar pinza', self.gripper_client, self.gripper_request(300.0)),
            ('Subir 205 mm', self.move_client, self.relative_z_request(220.0)),
            ('Abrir pinza', self.gripper_client, self.gripper_request(700.0)),
        ]

        if self.current_step >= len(steps):
            self.finish_grasping()
            return

        label, client, request = steps[self.current_step]

        if not client.service_is_ready():
            self.fail_grasping(f'Servicio no disponible: {client.srv_name}')
            return

        self.get_logger().info(f'Paso {self.current_step + 1}/{len(steps)}: {label}')

        self.command_in_progress = True
        future = client.call_async(request)
        future.add_done_callback(lambda f: self.step_callback(f, label))

    # ==================================================
    # RESPUESTA DE CADA OPERACIÓN
    # ==================================================

    def step_callback(self, future, label):
        self.command_in_progress = False

        if not self.active:
            return

        try:
            result = future.result()

            if result is None:
                self.fail_grasping(f'{label}: no se recibió respuesta.')
                return

            ret = getattr(result, 'ret', 0)

            if ret != 0:
                self.fail_grasping(f'{label}: el xArm devolvió ret={ret}.')
                return

            self.get_logger().info(f'{label}: operación completada.')

            self.current_step += 1
            self.execute_next_step()

        except Exception as e:
            self.fail_grasping(f'{label}: {e}')

    # ==================================================
    # CONSTRUCCIÓN DE PETICIONES
    # ==================================================

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

    def int16_request(self, value):
        req = SetInt16.Request()
        req.data = int(value)
        return req

    def float_request(self, value):
        req = SetFloat32.Request()
        req.data = float(value)
        return req

    def relative_z_request(self, delta_z):
        req = MoveCartesian.Request()
        req.pose = [0.0, 0.0, float(delta_z), 0.0, 0.0, 0.0]
        req.speed = 50.0
        req.acc = 500.0
        req.mvtime = 0.0
        req.relative = True
        req.is_tool_coord = False
        req.wait = True
        return req

    def gripper_request(self, position):
        req = GripperMove.Request()
        req.pos = float(position)
        req.wait = True
        return req

    # ==================================================
    # FINALIZACIÓN
    # ==================================================

    def finish_grasping(self):
        self.active = False

        self.get_logger().info('Grasping completado correctamente.')

        msg = String()
        msg.data = 'GRASPING_COMPLETE'
        self.transition_pub.publish(msg)

    def fail_grasping(self, reason):
        self.active = False
        self.command_in_progress = False

        self.get_logger().error(f'Grasping fallido: {reason}')

        msg = String()
        msg.data = 'GRASPING_FAILED'
        self.transition_pub.publish(msg)


def main(args=None):
    rclpy.init(args=args)
    node = GraspingNode()

    try:
        rclpy.spin(node)
    except KeyboardInterrupt:
        pass
    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()
