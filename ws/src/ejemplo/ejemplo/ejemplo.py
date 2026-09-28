import math

import rclpy
from rclpy.node import Node

from xarm_msgs.srv import MoveCartesian


class XArmPositionNode(Node):

    def __init__(self):
        super().__init__('xarm_position_node')

        # Cliente del Servicio de movimiento cartesiano
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

        # Primera posición inmediatamente
        self.send_position()

    # Callback: timer
    def send_position(self):

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
