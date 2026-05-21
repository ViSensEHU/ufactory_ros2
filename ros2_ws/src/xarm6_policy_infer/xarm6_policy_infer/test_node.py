#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import numpy as np
#import torch

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint

from pathlib import Path


class XarmPolicyNode(Node):
    def __init__(self):
        super().__init__("xarm_policy_node")

        # ---------------------------------------------------------
        # 1. Cargar modelo desde: <paquete>/models/model.pt
        # ---------------------------------------------------------
        pkg_root = Path(__file__).resolve().parent.parent.parent
        model_path = pkg_root / "models" / "agent.pt"

        self.get_logger().info(f"Cargando modelo desde: {model_path}")

        #self.policy = torch.jit.load(str(model_path))
        #self.policy.eval()

        # ---------------------------------------------------------
        # 2. Suscripciones ROS2
        # ---------------------------------------------------------
        self.create_subscription(JointState, "/joint_states", self.cb_joint_states, 10)
        self.create_subscription(PoseStamped, "/goal_pose", self.cb_goal_pose, 10)

        # ---------------------------------------------------------
        # 3. Publicador de trayectorias
        # ---------------------------------------------------------
        self.pub_traj = self.create_publisher(
            JointTrajectory,
            "/xarm6_traj_controller/joint_trajectory",
            10
        )

        # ---------------------------------------------------------
        # 4. Buffers internos
        # ---------------------------------------------------------
        self.joint_pos = None
        self.joint_vel = None
        self.goal_pose = None
        self.last_action = np.zeros(6)

        # ---------------------------------------------------------
        # 5. Normalización (igual que Isaac Lab)
        # ---------------------------------------------------------
        self.q_default = np.array([0.0, -0.15, -0.15, 0.0, 0.0, 0.0])
        self.action_scale = 0.5
        self.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]

        self.get_logger().info("Nodo de política del XArm6 iniciado correctamente.")

    # ============================================================
    # CALLBACKS
    # ============================================================

    def cb_joint_states(self, msg):
        self.joint_pos = np.array(msg.position[:6])
        self.joint_vel = np.array(msg.velocity[:6])
        self.try_infer()

    def cb_goal_pose(self, msg):
        self.goal_pose = np.array([
            msg.pose.position.x,
            msg.pose.position.y,
            msg.pose.position.z,
            0.0,
            3.14,
            0.0
        ])
        self.try_infer()

    # ============================================================
    # INFERENCIA
    # ============================================================

    def try_infer(self):
        if self.joint_pos is None or self.joint_vel is None or self.goal_pose is None:
            return

        # 1. Normalizar observaciones
        joint_pos_rel = (self.joint_pos - self.q_default) / self.action_scale
        joint_vel_rel = self.joint_vel

        # 2. Construir vector de observaciones
        obs = np.concatenate([
            joint_pos_rel,
            joint_vel_rel,
            self.goal_pose,
            self.last_action
        ])

        #obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)

        # 3. Inferencia
        #with torch.inference_mode():
        #    action = self.policy(obs_t).cpu().numpy()[0]
        #action = np.zeros(6)
        action = np.random.uniform(-1, 1, 6)

        # 4. Desnormalizar acción
        q_target = self.q_default + action * self.action_scale
        self.last_action = action

        # 5. Publicar JointTrajectory
        traj = JointTrajectory()
        traj.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = q_target.tolist()
        point.time_from_start.sec = 0
        point.time_from_start.nanosec = 200000000  # 0.2 s

        traj.points.append(point)
        self.pub_traj.publish(traj)

        self.get_logger().info(f"Acción enviada: {q_target}")


def main(args=None):
    rclpy.init(args=args)
    node = XarmPolicyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
