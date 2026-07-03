#!/usr/bin/env python3
import sys
import rclpy
from rclpy.node import Node

# Importar los tipos de servicio necesarios
from xarm_msgs.srv import SetInt16, MoveCartesian, MoveJoint


class DualArmTestNode(Node):
    def __init__(self):
        super().__init__('dual_arm_test_node')
        self.get_logger().info('Inicializando nodo de prueba dual: uFactory 850 + xArm...')

        # ── Cliente uFactory 850 (/ufactory/...) ──────────────────────────────
        self.cli_850_set_mode     = self.create_client(SetInt16,   '/ufactory/set_mode')
        self.cli_850_set_state    = self.create_client(SetInt16,   '/ufactory/set_state')
        self.cli_850_set_position = self.create_client(MoveCartesian, '/ufactory/set_position')
        self.cli_850_servo_angle  = self.create_client(MoveJoint,  '/ufactory/set_servo_angle')

        # ── Cliente xArm (/xarm/...) ─────────────────────────────────────────
        # Ajusta el namespace si tu xArm usa uno diferente (p.ej. /xarm6 o /robot2)
        self.cli_xarm_set_mode    = self.create_client(SetInt16,   '/xarm/set_mode')
        self.cli_xarm_set_state   = self.create_client(SetInt16,   '/xarm/set_state')
        self.cli_xarm_set_position = self.create_client(MoveCartesian, '/xarm/set_position')
        self.cli_xarm_servo_angle = self.create_client(MoveJoint,  '/xarm/set_servo_angle')

        self.wait_for_all_services()

    # ──────────────────────────────────────────────────────────────────────────
    def wait_for_all_services(self):
        clients = [
            (self.cli_850_set_mode,     '/ufactory/set_mode'),
            (self.cli_850_set_state,    '/ufactory/set_state'),
            (self.cli_850_set_position, '/ufactory/set_position'),
            (self.cli_850_servo_angle,  '/ufactory/set_servo_angle'),
            (self.cli_xarm_set_mode,    '/xarm/set_mode'),
            (self.cli_xarm_set_state,   '/xarm/set_state'),
            (self.cli_xarm_set_position,'/xarm/set_position'),
            (self.cli_xarm_servo_angle, '/xarm/set_servo_angle'),
        ]
        for client, name in clients:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Esperando al servicio {name}...')
        self.get_logger().info('Todos los servicios están disponibles.')

    # ──────────────────────────────────────────────────────────────────────────
    def call_services_parallel(self, calls: list[tuple]) -> list:
        """
        Lanza varios servicios en paralelo y espera a que todos respondan.

        Parámetro:
            calls: lista de tuplas (client, request, label)

        Retorna:
            Lista de resultados en el mismo orden que `calls`.
        """
        futures = []
        for client, request, label in calls:
            self.get_logger().info(f'  → Enviando: {label}')
            futures.append((client.call_async(request), label))

        results = []
        for future, label in futures:
            rclpy.spin_until_future_complete(self, future)
            result = future.result()
            self.get_logger().info(f'  ← Respuesta [{label}]: {result}')
            results.append(result)

        return results

    # ──────────────────────────────────────────────────────────────────────────
    def run_test_sequence(self):
        try:
            # ── PASO 1: Configurar Modo en ambos robots (paralelo) ─────────────
            self.get_logger().info('── PASO 1: Configurando modo 0 en ambos robots ──')
            req_mode_850  = SetInt16.Request(); req_mode_850.data  = 0
            req_mode_xarm = SetInt16.Request(); req_mode_xarm.data = 0
            self.call_services_parallel([
                (self.cli_850_set_mode,  req_mode_850,  '850 set_mode'),
                (self.cli_xarm_set_mode, req_mode_xarm, 'xArm set_mode'),
            ])

            # ── PASO 2: Configurar Estado en ambos robots (paralelo) ───────────
            self.get_logger().info('── PASO 2: Configurando estado 0 en ambos robots ──')
            req_state_850  = SetInt16.Request(); req_state_850.data  = 0
            req_state_xarm = SetInt16.Request(); req_state_xarm.data = 0
            self.call_services_parallel([
                (self.cli_850_set_state,  req_state_850,  '850 set_state'),
                (self.cli_xarm_set_state, req_state_xarm, 'xArm set_state'),
            ])

            # ── PASO 3: Primer movimiento simultáneo ──────────────────────────
            self.get_logger().info('── PASO 3: Movimiento 1 (simultáneo) ──')

            req_j850_1 = MoveJoint.Request()
            req_j850_1.angles  = [-0.58, 0.0, 0.0, 0.0, 0.0, 0.0]
            req_j850_1.speed   = 0.35
            req_j850_1.acc     = 10.0
            req_j850_1.mvtime  = 0.0

            req_jxarm_1 = MoveJoint.Request()
            req_jxarm_1.angles  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]  
            req_jxarm_1.speed   = 0.35
            req_jxarm_1.acc     = 10.0
            req_jxarm_1.mvtime  = 0.0

            self.call_services_parallel([
                (self.cli_850_servo_angle,  req_j850_1,  '850 movimiento 1'),
                (self.cli_xarm_servo_angle, req_jxarm_1, 'xArm movimiento 1'),
            ])

            # ── PASO 4: Segundo movimiento simultáneo ─────────────────────────
            self.get_logger().info('── PASO 4: Movimiento 2 (simultáneo) ──')

            req_j850_2 = MoveJoint.Request()
            req_j850_2.angles  = [0.58, 0.0, 0.0, 0.0, 0.0, 0.0]
            req_j850_2.speed   = 0.35
            req_j850_2.acc     = 10.0
            req_j850_2.mvtime  = 0.0

            req_jxarm_2 = MoveJoint.Request()
            req_jxarm_2.angles  = [0.0, -0.4904, -1.0227, 0.0, 1.4923, -0.6632]  
            req_jxarm_2.speed   = 0.35
            req_jxarm_2.acc     = 10.0
            req_jxarm_2.mvtime  = 0.0

            self.call_services_parallel([
                (self.cli_850_servo_angle,  req_j850_2,  '850 movimiento 2'),
                (self.cli_xarm_servo_angle, req_jxarm_2, 'xArm movimiento 2'),
            ])

            # ── PASO 5: Movimiento final exclusivo del xArm6 ─────────────────
            self.get_logger().info('── PASO 5: Regresando xArm6 a Home (aislado) ──')
            
            req_jxarm_home = MoveJoint.Request()
            req_jxarm_home.angles  = [0.0, 0.0, 0.0, 0.0, 0.0, 0.0]
            req_jxarm_home.speed   = 0.35
            req_jxarm_home.acc     = 10.0
            req_jxarm_home.mvtime  = 0.0

            self.call_services_parallel([
                (self.cli_xarm_servo_angle, req_jxarm_home, 'xArm6 regreso a Home'),
            ])

            self.get_logger().info('¡Secuencia de prueba dual finalizada con éxito!')

        except Exception as e:
            self.get_logger().error(f'Error durante la ejecución: {str(e)}')


# ──────────────────────────────────────────────────────────────────────────────
def main(args=None):
    rclpy.init(args=args)
    node = DualArmTestNode()

    node.run_test_sequence()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()