"""
prueba_motor_lineal.py
==========================
Script ROS 2 para mover de forma SIMULTÁNEA el motor lineal 
y el brazo xArm6 mediante llamadas de servicios en paralelo.
"""

import rclpy
import time
import math
from rclpy.node import Node

# Importamos los tipos de servicio necesarios para motor lineal y brazo cartesiano
from xarm_msgs.srv import (
    SetInt16,
    SetInt16ById,
    LinearMotorSetPos,
    LinearMotorBackOrigin,
    MoveCartesian,
)

# ---------------------------------------------------------------------------
# Parámetros globales de movimiento
# ---------------------------------------------------------------------------
LINEAR_SPEED       = 200    # mm/s
LINEAR_POS_DETECT  = 60    # mm
LINEAR_POS_RELEASE = 650    # mm

ARM_SPEED          = 100.0  # mm/s
ARM_ACC            = 2000.0 # mm/s^2


# ---------------------------------------------------------------------------
# Nodo de Control de Movimiento Simultáneo
# ---------------------------------------------------------------------------
class LinearMotorXArmNode(Node):

    def __init__(self):
        super().__init__('linear_motor_xarm_node')
        self.get_logger().info('Inicializando nodo de control simultáneo (Brazo + Motor)...')

        # ── Clientes para el Motor Lineal ──────────────────────────────────────
        self.cli_lin_enable = self.create_client(SetInt16, '/xarm/set_linear_motor_enable')
        self.cli_lin_speed  = self.create_client(SetInt16, '/xarm/set_linear_motor_speed')
        self.cli_lin_origin = self.create_client(LinearMotorBackOrigin, '/xarm/set_linear_motor_back_origin')
        self.cli_lin_pos    = self.create_client(LinearMotorSetPos, '/xarm/set_linear_motor_pos')

        # ── Clientes para el Brazo (xArm6) ──────────────────────────────────────
        self.cli_arm_mode     = self.create_client(SetInt16, '/xarm/set_mode')
        self.cli_arm_state    = self.create_client(SetInt16, '/xarm/set_state')
        self.cli_arm_position = self.create_client(MoveCartesian, '/xarm/set_position')
        self.cli_arm_motion_enable = self.create_client(SetInt16ById, '/xarm/motion_enable')

        self._wait_all_services()

    def _wait_all_services(self):
        services = [
            (self.cli_lin_enable, '/xarm/set_linear_motor_enable'),
            (self.cli_lin_speed,  '/xarm/set_linear_motor_speed'),
            (self.cli_lin_origin, '/xarm/set_linear_motor_back_origin'),
            (self.cli_lin_pos,    '/xarm/set_linear_motor_pos'),
            (self.cli_arm_mode,     '/xarm/set_mode'),
            (self.cli_arm_state,    '/xarm/set_state'),
            (self.cli_arm_position, '/xarm/set_position'),
            (self.cli_arm_motion_enable, '/xarm/motion_enable'),
        ]
        for client, name in services:
            while not client.wait_for_service(timeout_sec=1.0):
                self.get_logger().info(f'Esperando servicio {name}...')
        self.get_logger().info('Todos los servicios necesarios del sistema están listos.')

    def call_services_parallel(self, calls: list[tuple]) -> list:
        """
        Lanza múltiples peticiones de servicio asíncronas y bloquea el flujo
        hasta que todas se completen de manera concurrente.
        """
        futures = []
        for client, request, label in calls:
            self.get_logger().info(f'  → Enviando: {label}')
            futures.append((client.call_async(request), label))

        results = []
        for future, label in futures:
            rclpy.spin_until_future_complete(self, future)
            result = future.result()
            self.get_logger().info(f'  ← Respuesta [{label}]: ret={result.ret if result else "None"}')
            results.append(result)

        return results

    # ------------------------------------------------------------------
    # Secuencia de ejecución integrada
    # ------------------------------------------------------------------
    def run_sequence(self):
        self.get_logger().info('═══ INICIO DE SECUENCIA COORDENADA Y SIMULTÁNEA ═══')

        # ── PASO 1: Habilitación de motor lineal y brazo xArm (Paralelo) ──────────────────
        self.get_logger().info('PASO 1: Configurando modos y activando motor lineal...')
        
        req_lin_enable = SetInt16.Request(); req_lin_enable.data = 1 
        req_arm_motion_enable = SetInt16ById.Request(); req_arm_motion_enable.id = 8; req_arm_motion_enable.data = 1

        self.call_services_parallel([
            (self.cli_lin_enable, req_lin_enable, 'Habilitar Motor Lineal'),
            (self.cli_arm_motion_enable, req_arm_motion_enable, 'Habilitar Movimiento del Brazo'),
        ])
        time.sleep(1.0)

        # ── PASO 2: Estados y Búsqueda de Origen del Eje Lineal ──────────────
        self.get_logger().info('PASO 2: Colocando brazo en estado Ready y buscando origen del motor...')
        
        req_arm_mode   = SetInt16.Request(); req_arm_mode.data   = 0  # Modo Cartesiano de fábrica
        req_lin_origin = LinearMotorBackOrigin.Request()
        req_lin_origin.wait = True
        req_lin_origin.auto_enable = True

        self.call_services_parallel([
            (self.cli_arm_mode,   req_arm_mode,   'Configurar Brazo (Modo 0)'),
            (self.cli_lin_origin,   req_lin_origin, 'Motor Lineal a Origen'),
        ])

        # Configurar velocidades iniciales de trabajo y estado del brazo robotico
        req_lin_speed = SetInt16.Request(); req_lin_speed.data = LINEAR_SPEED
        req_arm_state  = SetInt16.Request(); req_arm_state.data = 0   # Estado Ready para moverse
        
        self.call_services_parallel([
            (self.cli_lin_speed, req_lin_speed, 'Set velocidad motor'),
            (self.cli_arm_state, req_arm_state, 'Set estado brazo')
        ])

        # ── PASO 3: Primer Movimiento Simultáneo (Detección / Pick) ─────────
        self.get_logger().info('PASO 3: Moviendo motor lineal a Posición 1 y Brazo a coordenadas de aproximación...')

        # Petición para el Motor Lineal
        req_move_lin_1 = LinearMotorSetPos.Request()
        req_move_lin_1.pos         = LINEAR_POS_DETECT
        req_move_lin_1.speed       = LINEAR_SPEED
        req_move_lin_1.wait        = True
        req_move_lin_1.auto_enable = True

        # Petición Cartesiana para el Brazo (x, y, z, roll, pitch, yaw)
        req_move_arm_1 = MoveCartesian.Request()
        req_move_arm_1.pose   = [220.5, 0.0, 575.0, math.radians(180), math.radians(0), math.radians(0)]
        req_move_arm_1.speed  = ARM_SPEED
        req_move_arm_1.acc    = ARM_ACC
        req_move_arm_1.mvtime = 0.0
        req_move_arm_1.wait   = True

        # Se lanzan los dos comandos de movimiento en paralelo al bus TCP
        self.call_services_parallel([
            (self.cli_lin_pos,      req_move_lin_1, 'Motor a Pos_Detect (60mm)'),
            (self.cli_arm_position, req_move_arm_1, 'Brazo a Pose_Aproximacion'),
        ])
        
        self.get_logger().info('Llegada al punto de detección simultánea completada. Esperando 2s...')
        time.sleep(2.0)

        # ── PASO 4: Segundo Movimiento Simultáneo (Entrega / Release) ───────
        self.get_logger().info('PASO 4: Moviendo motor lineal a Posición 2 y Brazo a coordenadas de entrega...')

        # Petición para el Motor Lineal
        req_move_lin_2 = LinearMotorSetPos.Request()
        req_move_lin_2.pos         = LINEAR_POS_RELEASE
        req_move_lin_2.speed       = LINEAR_SPEED
        req_move_lin_2.wait        = True
        req_move_lin_2.auto_enable = True

        # Petición Cartesiana para el Brazo
        req_move_arm_2 = MoveCartesian.Request()
        req_move_arm_2.pose   = [0.0, 360.5, 488.0, math.radians(180), math.radians(0), math.radians(0)]
        req_move_arm_2.speed  = ARM_SPEED
        req_move_arm_2.acc    = ARM_ACC
        req_move_arm_2.mvtime = 0.0
        req_move_arm_2.wait   = True

        # Se lanzan en paralelo
        self.call_services_parallel([
            (self.cli_lin_pos,      req_move_lin_2, 'Motor a Pos_Release (650mm)'),
            (self.cli_arm_position, req_move_arm_2, 'Brazo a Pose_Entrega'),
        ])

        # Petición Cartesiana para el Brazo
        req_move_arm_3 = MoveCartesian.Request()
        req_move_arm_3.pose   = [0.0, 360.5, 488.0, math.radians(71.5), math.radians(-90), math.radians(-161.8)]
        req_move_arm_3.speed  = ARM_SPEED
        req_move_arm_3.acc    = ARM_ACC
        req_move_arm_3.mvtime = 0.0
        req_move_arm_3.wait   = True

        self.call_services_parallel([
            (self.cli_arm_position, req_move_arm_3, 'Brazo a Pose_PostEntrega'),
        ])

        self.get_logger().info('═══ SECUENCIA SIMULTÁNEA FINALIZADA CON ÉXITO ═══')


# ---------------------------------------------------------------------------
# Entrada del Script
# ---------------------------------------------------------------------------
def main(args=None):
    rclpy.init(args=args)
    node = LinearMotorXArmNode()

    node.run_sequence()

    node.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()