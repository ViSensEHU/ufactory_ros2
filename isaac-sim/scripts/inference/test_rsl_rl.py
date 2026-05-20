import numpy as np
import torch

# -----------------------------
# CONFIGURACIÓN DEL MODELO
# -----------------------------
MODEL_PATH = "exported/policy.pt"
ACTION_SCALE = 0.5

# q_default debe tener 12 valores (6 actuados + 6 mimics/fijos)
q_default_full = np.array([
    0.0, -0.15, -0.15, 0.0, 0.0, 0.0,   # tus 6 DOF reales
    0.0, 0.0, 0.0, 0.0, 0.0, 0.0        # 6 joints mimics/fijos
], dtype=np.float32)

# -----------------------------
# CARGAR MODELO
# -----------------------------
print("Cargando modelo...")
policy = torch.jit.load(MODEL_PATH)
policy.eval()
print("Modelo cargado correctamente.")

# -----------------------------
# ESTADO ARTICULAR REAL (solo 6 DOF)
# -----------------------------
joint_pos_6 = np.array([0.1, -0.2, -0.1, 0.05, 0.0, 0.0], dtype=np.float32)
joint_vel_6 = np.zeros(6, dtype=np.float32)

# Expandir a 12 DOF (añadir ceros para mimics/fijos)
joint_pos_12 = np.concatenate([joint_pos_6, np.zeros(6)], axis=0)
joint_vel_12 = np.concatenate([joint_vel_6, np.zeros(6)], axis=0)

# -----------------------------
# GOAL POSE (7 valores)
# -----------------------------
import math
from scipy.spatial.transform import Rotation as R
import numpy as np

goal_pose_7 = np.zeros(7, dtype=np.float32)

# Posición objetivo
goal_pose_7[0] = 0.45
goal_pose_7[1] = 0.0
goal_pose_7[2] = 0.25

# Orientación objetivo en Euler (roll, pitch, yaw)
roll  = 0.0
pitch = math.pi
yaw   = 0.0

# Convertir a cuaternión (qx, qy, qz, qw)
qx, qy, qz, qw = R.from_euler('xyz', [roll, pitch, yaw]).as_quat()

goal_pose_7[3] = qx
goal_pose_7[4] = qy
goal_pose_7[5] = qz
goal_pose_7[6] = qw


# -----------------------------
# ACCIÓN PREVIA (6 valores)
# -----------------------------
last_action = np.zeros(6, dtype=np.float32)

# -----------------------------
# CONSTRUIR OBSERVACIÓN (37)
# -----------------------------
joint_pos_rel_12 = (joint_pos_12 - q_default_full) / ACTION_SCALE

obs = np.concatenate([
    joint_pos_rel_12,   # 12
    joint_vel_12,       # 12
    goal_pose_7,        # 7
    last_action         # 6
], axis=0).astype(np.float32)

print("Dimensión de obs:", obs.shape)
print("Obs =", obs)

# -----------------------------
# INFERENCIA
# -----------------------------
obs_t = torch.tensor(obs, dtype=torch.float32).unsqueeze(0)

with torch.inference_mode():
    action = policy(obs_t).cpu().numpy()[0]

print("\n=== RESULTADOS DE LA POLÍTICA ===")
print("Acción normalizada:", action)

# -----------------------------
# DESNORMALIZAR ACCIÓN
# -----------------------------
q_target = q_default_full[:6] + action * ACTION_SCALE
print("q_target:", q_target)
