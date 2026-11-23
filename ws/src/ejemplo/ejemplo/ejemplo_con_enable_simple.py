import math

import rclpy
from rclpy.node import Node

from xarm_msgs.srv import MoveCartesian, SetInt16, SetInt16ById   # ← AÑADIDO


class XArmPositionNode(Node):

    def __init__(self):
        super().__init__('xarm_position_node')

        # Namespace del robot: 'xarm' para el xArm6, 'ufactory' para el UF850
        self.hw_ns = self.declare_parameter('hw_ns', 'xarm').value

        # Cliente del Servicio de movimiento cartesiano
        self.move_client = self.create_client(
            MoveCartesian,
            f'/{self.hw_ns}/set_position'
        )

        while not self.move_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info(
                f'Esperando al servicio /{self.hw_ns}/set_position...'
            )

        self.get_logger().info(
            f'Servicio /{self.hw_ns}/set_position disponible.'
        )

        # ══════════════════════ AÑADIDO ══════════════════════
        self.enable_client = self.create_client(
            SetInt16ById, f'/{self.hw_ns}/motion_enable')
        self.mode_client = self.create_client(
            SetInt16, f'/{self.hw_ns}/set_mode')
        self.state_client = self.create_client(
            SetInt16, f'/{self.hw_ns}/set_state')

        for cliente in (self.enable_client, self.mode_client, self.state_client):
            while not cliente.wait_for_service(timeout_sec=1.0):
                self.get_logger().info('Esperando servicios de configuración...')

        self.ready = False      # todavía no se puede mover
        # ═════════════════════════════════════════════════════

        # Posiciones
        self.pose = [
            300.0,     # X [mm]
            0.0,       # Y [mm]
            400.0,     # Z [mm]
            math.pi,   # Roll
            0.0,       # Pitch
            0.0        # Yaw
        ]

        # Timer de ROS2: cada 2 segundos
        self.timer = self.create_timer(
            2.0,
            self.send_position
        )

        # Primera posición inmediatamente (tras configurar el robot)
        self._configurar()        # ← CAMBIADO (antes: self.send_position())

    # ══════════════════════════ AÑADIDO ══════════════════════════
    # Se hace en cadena a mano: lanzo una orden y, cuando contesta,
    # lanzo la siguiente. Así se respeta el orden enable -> mode -> state
    # sin bloquear el nodo.
    def _configurar(self):
        """Paso 1: habilitar todos los ejes."""
        req = SetInt16ById.Request()
        req.id = 8        # 8 = todos los ejes
        req.data = 1      # 1 = habilitar
        self.enable_client.call_async(req).add_done_callback(self._configurar_modo)

    def _configurar_modo(self, future):
        """Contesta motion_enable -> Paso 2: modo 0 (posición)."""
        self.get_logger().info(f'motion_enable -> ret={future.result().ret}')
        req = SetInt16.Request()
        req.data = 0
        self.mode_client.call_async(req).add_done_callback(self._configurar_estado)

    def _configurar_estado(self, future):
        """Contesta set_mode -> Paso 3: estado 0 (listo)."""
        self.get_logger().info(f'set_mode -> ret={future.result().ret}')
        req = SetInt16.Request()
        req.data = 0
        self.state_client.call_async(req).add_done_callback(self._listo)

    def _listo(self, future):
        """Contesta set_state -> el robot ya se puede mover."""
        self.get_logger().info(f'set_state -> ret={future.result().ret}')
        self.ready = True
        self.send_position()      # primera posición
    # ═════════════════════════════════════════════════════════════

    # Callback: timer
    def send_position(self):

        # ← AÑADIDO: no mover nada hasta que esté configurado
        if not self.ready:
            return

        self.get_logger().info(
            f'Enviando posición: {self.pose}'
        )

        self.set_position(self.pose)

        # Después de mandar la primera posición,
        # cambiamos Z para el siguiente envío.
        if self.pose[2] == 400.0:
            self.pose[2] = 250.0

        else:
            self.pose[2] = 400.0

            # Si queremos parar el timer
            #self.timer.cancel()

    # Método para encapsular la llamada al servicio.
    # El proceso de este método equivale a
    """ 
    ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian 
    "{pose: [300, 0, 250, 3.14, 0, 0], speed: 50, acc: 500, mvtime: 0}"
    """ 
    def set_position(self, pose, speed=50.0, acc=500.0):
        req = MoveCartesian.Request()
        req.pose = [
            float(value)
            for value in pose
        ]
        req.speed = float(speed)
        req.acc = float(acc)
        req.mvtime = 0.0
        req.wait = False

        # Llamada asíncrona al método (no bloquea el nodo
        # esperando la respuesta)
        future = self.move_client.call_async(req)
        
        # Definir un método a ejecutar cuando se reciba
        # la respuesta del servicio
        future.add_done_callback(
            self._movement_callback
        )

    def _movement_callback(self, future):
        try:
            response = future.result()
            if response is None:
                self.get_logger().error(
                    'El servicio no devolvió respuesta.'
                )
                return

            self.get_logger().info(
                'Orden de movimiento aceptada.'
            )

        except Exception as e:
            self.get_logger().error(
                f'Error ejecutando /xarm/set_position: {e}'
            )

def main(args=None):
    rclpy.init(args=args)
    node = XArmPositionNode()

    try:
        rclpy.spin(node)

    finally:
        node.destroy_node()
        rclpy.shutdown()

if __name__ == '__main__':
    main()