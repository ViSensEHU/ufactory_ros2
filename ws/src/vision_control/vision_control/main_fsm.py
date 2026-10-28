#!/usr/bin/env python3

import math
from enum import Enum

import rclpy
from rclpy.node import Node

from geometry_msgs.msg import Point

from lifecycle_msgs.srv import ChangeState
from lifecycle_msgs.msg import Transition

from xarm_msgs.srv import (MoveCartesian, GripperMove, SetInt16, SetInt16ById, SetFloat32)


class State(Enum):
    TRACKING = 0
    GRASPING = 1
    FINISHED = 2


class VisualGraspFSM(Node):

    def __init__(self):
        super().__init__('visual_grasp_fsm')

        self.state = State.TRACKING
        self.grasp_executed = False

        # --------------------------------------------------
        # Error visual
        # --------------------------------------------------
        self.error_u = 999.0
        self.error_v = 999.0

        self.deadband_px = 20

        self.center_counter = 0
        self.required_center_cycles = 10

        self.motion_enable_client = self.create_client(SetInt16ById, '/xarm/motion_enable')
        self.mode_client = self.create_client(SetInt16, '/xarm/set_mode')
        self.state_client = self.create_client(SetInt16, '/xarm/set_state')

        # --------------------------------------------------
        # Lifecycle controller
        # --------------------------------------------------
        self.change_state_client = self.create_client(ChangeState, '/xarm_visual_servo_controller/change_state')

        while not self.change_state_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando Lifecycle controller...')

        # --------------------------------------------------
        # MoveCartesian
        # --------------------------------------------------
        self.move_client = self.create_client(MoveCartesian, '/xarm/set_position')
        while not self.move_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando /xarm/set_position...')

        self.move_aa_client = self.create_client(MoveCartesian, '/xarm/set_position_aa')
        while not self.move_aa_client.wait_for_service(timeout_sec=1.0):
                    self.get_logger().info('Esperando /xarm/set_position_aa...')

        # --------------------------------------------------
        # Gripper
        # --------------------------------------------------
        self.gripper_enable_client = self.create_client(SetInt16, '/xarm/set_gripper_enable')
        self.gripper_mode_client = self.create_client(SetInt16, '/xarm/set_gripper_mode')
        self.gripper_speed_client = self.create_client(SetFloat32, '/xarm/set_gripper_speed')

        self.gripper_client = self.create_client(GripperMove, '/xarm/set_gripper_position')

        while not self.gripper_client.wait_for_service(timeout_sec=1.0):
            self.get_logger().info('Esperando /xarm/set_gripper_position...')

        # --------------------------------------------------
        # Error visual
        # --------------------------------------------------
        self.error_sub = self.create_subscription(Point, '/green_ball/error', self.error_callback, 10)

        # --------------------------------------------------
        # Pose objetivo
        # --------------------------------------------------
        self.pose = [300.0, 0.0, 400.0, math.pi, 0.0, 0.0]

        # --------------------------------------------------
        # Arrancar tracking
        # --------------------------------------------------
        self.motion_enable()
        self.set_xarm_mode(0)
        self.set_xarm_state(0)

        self.enable_gripper()
        self.set_gripper_mode(0)
        self.set_gripper_speed(1500.0)

        self.move_to_pose(self.pose)
        self.set_xarm_mode(7)
        self.set_xarm_state(0)

        self.lifecycle_transition(Transition.TRANSITION_CONFIGURE)
        self.lifecycle_transition(Transition.TRANSITION_ACTIVATE)

        self.get_logger().info('Tracking activado.')

        # --------------------------------------------------
        # FSM timer
        # --------------------------------------------------
        self.timer = self.create_timer(0.1, self.control_loop)

    def motion_enable(self):

        req = SetInt16ById.Request()
        req.id = 8
        req.data = 1

        future = self.motion_enable_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info('Motion enabled.')
    
    def set_xarm_mode(self, mode):

        req = SetInt16.Request()
        req.data = int(mode)

        future = self.mode_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(f'Modo xArm = {mode}')

    def set_xarm_state(self, state):

        req = SetInt16.Request()
        req.data = int(state)

        future = self.state_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(f'Estado xArm = {state}')

    def enable_gripper(self):

        req = SetInt16.Request()
        req.data = 1

        future = self.gripper_enable_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info('Gripper enabled.')

    def set_gripper_mode(self, mode=0):

        req = SetInt16.Request()
        req.data = int(mode)

        future = self.gripper_mode_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(f'Gripper mode = {mode}')

    def set_gripper_speed(self, speed=1500.0):

        req = SetFloat32.Request()
        req.data = float(speed)

        future = self.gripper_speed_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info(f'Gripper speed = {speed}')
    
    # ==================================================
    # Lifecycle helper
    # ==================================================
    def lifecycle_transition(self, transition_id):

        req = ChangeState.Request()
        req.transition.id = transition_id

        future = self.change_state_client.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        if future.result() is not None:
            self.get_logger().info(f'Transición {transition_id} ejecutada.')

        else:
            self.get_logger().error('Error haciendo transición.')

    # ==================================================
    # Error visual
    # ==================================================
    def error_callback(self, msg):

        self.error_u = float(msg.x)
        self.error_v = float(msg.y)

    # ==================================================
    # FSM
    # ==================================================
    def control_loop(self):

        if self.state == State.TRACKING:
            self.tracking_state()

        elif self.state == State.GRASPING:
            self.grasping_state()

        elif self.state == State.FINISHED:
            pass

    # ==================================================
    # TRACKING
    # ==================================================
    def tracking_state(self):

        centered = (abs(self.error_u) < self.deadband_px and abs(self.error_v) < self.deadband_px)

        if centered:
            self.center_counter += 1

        else:
            self.center_counter = 0

        if self.center_counter > self.required_center_cycles:
            self.get_logger().info('Objeto alineado.')
            self.lifecycle_transition(Transition.TRANSITION_DEACTIVATE)

            self.set_xarm_mode(0)
            self.set_xarm_state(0)

            self.state = State.GRASPING

    # ==================================================
    # GRASPING
    # ==================================================
    def grasping_state(self):

        if self.grasp_executed:
            return

        self.grasp_executed = True

        self.get_logger().info('Iniciando grasp.')

        # Bajar 205 mm
        self.move_relative_z(-205.0)

        # Cerrar pinza
        self.close_gripper(300.0)

        # Subir 205 mm
        self.move_relative_z(205.0)

        self.get_logger().info('Grasp completado.')

        self.state = State.FINISHED

    # ==================================================
    # Move Cartesian
    # ==================================================
    def move_to_pose(self, pose):

        req = MoveCartesian.Request()
        req.pose = pose
        req.speed = 50.0
        req.acc = 500.0
        req.mvtime = 0.0
        req.wait = True

        future = self.move_client.call_async(req)
        print("ESPERANDO FUTURE")
        rclpy.spin_until_future_complete(self, future)

    def move_relative_z(self, delta_z):

        req = MoveCartesian.Request()
        req.pose = [0.0, 0.0, float(delta_z), 0.0, 0.0, 0.0]

        req.speed = 50.0
        req.acc = 500.0
        req.relative = True
        req.is_tool_coord = True
        req.wait = True

        future = self.move_aa_client.call_async(req)
        rclpy.spin_until_future_complete(self, future)

        response = future.result()

        if response is not None:
            self.get_logger().info(f'Movimiento relativo Z={delta_z} mm completado.')

        else:
            self.get_logger().error('Error en movimiento relativo.')

    # ==================================================
    # Gripper
    # ==================================================
    def close_gripper(self, position):

        req = GripperMove.Request()
        req.pos = position
        future = self.gripper_client.call_async(req)

        rclpy.spin_until_future_complete(self, future)

        self.get_logger().info('Pinza cerrada.')


def main(args=None):

    rclpy.init(args=args)
    node = VisualGraspFSM()

    try:
        rclpy.spin(node)

    except KeyboardInterrupt:
        pass

    finally:
        node.destroy_node()
        rclpy.shutdown()


if __name__ == '__main__':
    main()