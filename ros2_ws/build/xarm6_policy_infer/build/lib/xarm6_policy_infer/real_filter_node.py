#!/usr/bin/env python3
import rclpy
from rclpy.node import Node

import numpy as np
import torch

from sensor_msgs.msg import JointState
from geometry_msgs.msg import PoseStamped
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint


class XarmPolicyNode(Node):
    def __init__(self):
        super().__init__("xarm_policy_node")

        # ---------------------------------------------------------
        # 1. Cargar modelo (TorchScript)
        # ---------------------------------------------------------
        model_path = "/home/isaac_sim/ros2_ws/src/xarm6_policy_infer/models/policy.pt"
        self.get_logger().info(f"Cargando modelo desde: {model_path}")
        self.policy = torch.jit.load(str(model_path))
        self.policy.eval()

        # ---------------------------------------------------------
        # 2. Suscripciones
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
        self.joint_pos = None          # 6 DOF reales
        self.joint_vel = None          # 6 DOF reales
        self.goal_pose = None          # 7 valores: x,y,z,qx,qy,qz,qw
        self.last_action = np.zeros(6, dtype=np.float32)
        self.last_q_target = None      # para suavizado

        # ---------------------------------------------------------
        # 5. Normalización y límites
        # ---------------------------------------------------------
        self.action_scale = 0.2  # más conservador que 0.5 para empezar

        self.q_default_full = np.array([
            0.0, -0.15, -0.15, 0.0, 0.0, 0.0,   # 6 DOF reales
            0.0, 0.0, 0.0, 0.0, 0.0, 0.0        # 6 mimics/fijos
        ], dtype=np.float32)

        self.q_default_6 = self.q_default_full[:6]

        self.joint_lower = np.array([-2.9, -1.7, -2.9, -3.1, -2.0, -3.1], dtype=np.float32)
        self.joint_upper = np.array([ 2.9,  1.7,  2.9,  3.1,  2.0,  3.1], dtype=np.float32)

        self.joint_names = ["joint1", "joint2", "joint3", "joint4", "joint5", "joint6"]

        # ---------------------------------------------------------
        # 6. Control loop (timer) + decimation
        # ---------------------------------------------------------
        self.control_dt = 0.02   # 50 Hz
        self.decimation = 4      # política a 12.5 Hz
        self.step_counter = 0

        self.timer = self.create_timer(self.control_dt, self.control_loop)

        self.get_logger().info("Nodo de política del XArm6 iniciado correctamente.")

    # ============================================================
    # CALLBACKS
    # ============================================================

    def cb_joint_states(self, msg: JointState):
        self.joint_pos = np.array(msg.position[:6], dtype=np.float32)
        if msg.velocity:
            self.joint_vel = np.array(msg.velocity[:6], dtype=np.float32)
        else:
            self.joint_vel = np.zeros(6, dtype=np.float32)

    def cb_goal_pose(self, msg: PoseStamped):
        x = msg.pose.position.x
        y = msg.pose.position.y
        z = msg.pose.position.z

        qx = msg.pose.orientation.x
        qy = msg.pose.orientation.y
        qz = msg.pose.orientation.z
        qw = msg.pose.orientation.w

        self.goal_pose = np.array([x, y, z, qx, qy, qz, qw], dtype=np.float32)

    # ============================================================
    # CONTROL LOOP
    # ============================================================

    def control_loop(self):
        # Esperar a tener todo
        if self.joint_pos is None or self.joint_vel is None or self.goal_pose is None:
            return

        # -----------------------------
        # 1. Expandir a 12 DOF
        # -----------------------------
        joint_pos_12 = np.concatenate([self.joint_pos, np.zeros(6, dtype=np.float32)], axis=0)
        joint_vel_12 = np.concatenate([self.joint_vel, np.zeros(6, dtype=np.float32)], axis=0)

        # -----------------------------
        # 2. Normalizar posiciones (igual que antes)
        #    OJO: si en entrenamiento NO se dividía por action_scale,
        #         aquí habría que quitar esa división.
        # -----------------------------
        joint_pos_rel_12 = (joint_pos_12 - self.q_default_full) / self.action_scale

        # -----------------------------
        # 3. Construir observación (37)
        # -----------------------------
        obs = np.concatenate([
            joint_pos_rel_12,      # 12
            joint_vel_12,          # 12
            self.goal_pose,        # 7
            self.last_action       # 6
        ], axis=0).astype(np.float32)

        # -----------------------------
        # 4. Decimation: solo inferir cada N pasos
        # -----------------------------
        if self.step_counter % self.decimation == 0:
            obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)
            with torch.inference_mode():
                action = self.policy(obs_t).cpu().numpy()[0]   # 6 valores
            self.last_action = action
        else:
            action = self.last_action

        # -----------------------------
        # 5. Desnormalizar → q_raw (6 DOF)
        # -----------------------------
        q_raw = self.q_default_6 + action * self.action_scale

        # -----------------------------
        # 6. Suavizado (blending)
        # -----------------------------
        if self.last_q_target is None:
            q_target = q_raw
        else:
            alpha = 0.2  # suavizado; más bajo = más suave
            q_target = alpha * q_raw + (1.0 - alpha) * self.last_q_target

        q_target = np.clip(q_target, self.joint_lower, self.joint_upper)
        self.last_q_target = q_target.copy()

        # -----------------------------
        # 7. Publicar JointTrajectory
        # -----------------------------
        traj = JointTrajectory()
        traj.joint_names = self.joint_names

        point = JointTrajectoryPoint()
        point.positions = q_target.tolist()
        # Dar tiempo suficiente para llegar (suave)
        point.time_from_start.sec = 1
        point.time_from_start.nanosec = 0

        traj.points.append(point)
        self.pub_traj.publish(traj)

        # Opcional: log más ligero
        # self.get_logger().info(f"q_target: {q_target}")

        self.step_counter += 1


def main(args=None):
    rclpy.init(args=args)
    node = XarmPolicyNode()
    rclpy.spin(node)
    node.destroy_node()
    rclpy.shutdown()


if __name__ == "__main__":
    main()
