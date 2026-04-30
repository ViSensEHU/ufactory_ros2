import torch
import isaaclab.sim as sim_utils
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg, IdealPDActuatorCfg
from isaaclab.assets import AssetBaseCfg
from isaaclab.utils import configclass

from pathlib import Path

# Ruta relativa
BASE_DIR = Path(__file__).resolve().parent
USD_PATH = str(BASE_DIR / "usd" / "xarm6_instanciable.usd")
# ------------------

# --- Configuración del robot ---
XARM6_CONFIG = ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(usd_path=USD_PATH),
    init_state=ArticulationCfg.InitialStateCfg( # Posiciones iniciales
        pos=(0.0, 0.0, 0.05),                   # Motor lineal completamente sobre el plano
        joint_pos={
            "joint1": 0.0,
            "joint2": -0.15,
            "joint3": -0.15,
            "joint4": 0.0,
            "joint5": 0.0,
            "joint6": 0.0,
            "drive_joint": 0.0,
        },
    ),
    actuators = {
        # PD para todas las articulaciones del brazo (joint1–joint6)
        "arm_pd": ImplicitActuatorCfg(
            joint_names_expr=["joint.*"],  # joint1, joint2, ..., joint6
            stiffness=None,#200.0,               # puedes subir a 300–400 si va muy blando
            damping=None,#20.0,                  # si vibra, sube a 30–40
        ),
    }
)
# -------------------------------

"""

        # PD para el motor lineal
        "linear_pd": IdealPDActuatorCfg(
            joint_names_expr=["Component2_to_BaseLink"],
            stiffness=None, #4000.0,              # más alto porque es prismatic y suele ser más rígido
            damping=None, #200.0,                 # suficiente para amortiguar
        ),
"""