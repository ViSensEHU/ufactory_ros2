import argparse
from isaaclab.app import AppLauncher

parser = argparse.ArgumentParser()
parser.add_argument("--num_envs", type=int, default=4)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import torch
import isaaclab.sim as sim_utils
from isaaclab.scene import InteractiveScene, InteractiveSceneCfg
from isaaclab.assets.articulation import ArticulationCfg
from isaaclab.actuators import ImplicitActuatorCfg, IdealPDActuatorCfg
from isaaclab.assets import AssetBaseCfg
from isaaclab.utils import configclass

from pathlib import Path

# --- Cargar USD ---
# Ruta absoluta
# USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/scripts/usd/xarm6_visens.usd" 

# Ruta relativa
BASE_DIR = Path(__file__).resolve().parent
USD_PATH = str(BASE_DIR / "usd" / "xarm6_visens.usd")
# ------------------

# --- Configuración del robot ---
XARM6_CONFIG = ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(usd_path=USD_PATH),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.05),
        rot=(0.7071068, 0.7071068, 0.0, 0.0),
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
    actuators={
        "joint1": ImplicitActuatorCfg(
            joint_names_expr=["joint1"],
            stiffness=None,#73.29828, #Con None no se modifica nada del USD.
            damping=None,#0.02932,
        ),
        "joint2": ImplicitActuatorCfg(
            joint_names_expr=["joint2"],
            stiffness=None,#114.32549,
            damping=None,#0.04573,
        ),
        "joint3": ImplicitActuatorCfg(
            joint_names_expr=["joint3"],
            stiffness=None,#95.28044,
            damping=None,#0.03811,
        ),
        "joint4": ImplicitActuatorCfg(
            joint_names_expr=["joint4"],
            stiffness=None,#283.06,
            damping=None,#0.11322,
        ),
        "joint5": ImplicitActuatorCfg(
            joint_names_expr=["joint5"],
            stiffness=None,#9.7635,
            damping=None,#0.00391,
        ),
        "joint6": ImplicitActuatorCfg(
            joint_names_expr=["joint6"],
            stiffness=None,#2.07821,
            damping=None,#0.00083,
        ),
        "drive_joint": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            stiffness=None,#0.54539,
            damping=None,#0.00022,
        ),
        "linear_motor": ImplicitActuatorCfg(
            joint_names_expr=["Component2_to_BaseLink"],
            stiffness=None,#16000.0,
            damping=None,#2800.0,
        ),
    }
)
#UsdFileCfg
"""rigid_props=sim_utils.RigidBodyPropertiesCfg(
            disable_gravity=False,
            max_depenetration_velocity=5.0,
        ),
        articulation_props=sim_utils.ArticulationRootPropertiesCfg(
            articulation_enabled=True,
            enabled_self_collisions=True, 
            solver_position_iteration_count=32, 
            solver_velocity_iteration_count=1,
            sleep_threshold=0.005,
            stabilization_threshold=0.001
        ),"""

# IdealPDActuatorCfg
"""XARM6_CONFIG = ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(usd_path=USD_PATH),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.1),
    ),
    actuators={
        "arm": IdealPDActuatorCfg(
            joint_names_expr=["joint[1-6]"],
            stiffness=None,        # usa stiffness del USD
            damping=None,          # usa damping del USD
            effort_limit=None,     # usa maxForce del USD
            velocity_limit=None,   # usa velocity limit del USD
        )
    }
)"""
# -------------------------------


# --- Configuración de la escena ---
@configclass
class Xarm6SceneCfg(InteractiveSceneCfg):
    # Plano del suelo
    ground = AssetBaseCfg(
        prim_path="/World/Ground",
        spawn=sim_utils.GroundPlaneCfg()
    )

    # Luz de la escena
    light = AssetBaseCfg(
        prim_path="/World/Light",
        spawn=sim_utils.DomeLightCfg(intensity=3000.0)
    )

    # Robot con la configuración definida arriba
    robot = XARM6_CONFIG
# ----------------------------------

# --- Ejecución de la simulación ---
def run_sim(sim, scene):
    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0

    while simulation_app.is_running():

        if count % 100 == 0:
            # Reset a los 100 steps
            print("[INFO] Resetting robots...")
            count = 0

            """Root en posición inicial, es decir,
                    init_state=ArticulationCfg.InitialStateCfg(
                    pos=(0.0, 0.0, 0.05),
                    rot=(0.7071068, 0.7071068, 0.0, 0.0),"""
            root = scene["robot"].data.default_root_state.clone()
            root[:, :3] += scene.env_origins
            scene["robot"].write_root_pose_to_sim(root[:, :7])
            scene["robot"].write_root_velocity_to_sim(root[:, 7:])

            """Articulaciones en posiciones iniciales, es decir,
                    joint_pos={
                        "joint1": 0.0,
                        "joint2": -0.15,
                        "joint3": -0.15,
                        "joint4": 0.0,
                        "joint5": 0.0,
                        "joint6": 0.0,
                        "drive_joint": 0.0,
                    },"""
            jpos = scene["robot"].data.default_joint_pos.clone()
            jvel = scene["robot"].data.default_joint_vel.clone()
            scene["robot"].write_joint_state_to_sim(jpos, jvel)

            scene.reset()

        
        # Obtener los nombres e índices de las joints
        joint_names = scene["robot"].joint_names 
        joint_indices = list(range(len(joint_names)))
        joint_idx_map = {name: idx for idx, name in enumerate(joint_names)}

        # Crear el array de posiciones articulares objetivo
        target_pos = scene["robot"].data.default_joint_pos.clone()
        target_pos[:, joint_idx_map["joint1"]] = 0.4
        target_pos[:, joint_idx_map["joint2"]] = 0.0
        target_pos[:, joint_idx_map["joint3"]] = -0.5
        target_pos[:, joint_idx_map["joint4"]] = 0.0
        target_pos[:, joint_idx_map["joint5"]] = 0.0
        target_pos[:, joint_idx_map["joint6"]] = 0.0
        target_pos[:, joint_idx_map["drive_joint"]] = 0.5
        target_pos[:, joint_idx_map["Component2_to_BaseLink"]] = 0.3

        scene["robot"].set_joint_position_target(target_pos)
        # ---------------------------------------------------------

        scene.write_data_to_sim()
        sim.step()
        scene.update(sim_dt)

        sim_time += sim_dt
        count += 1
        # convertir sim_time → tensor
        #t = torch.tensor(sim_time, device=target_pos.device)
        # joint1 → movimiento sinusoidal suave
        #target_pos[:, 0] = 0.7854 #1.5708 #0.5 * torch.sin(2 * torch.pi * 0.5 * t)
        # Mover drive_joint con un seno
        #target_pos[:, 6] = 0.0#0.3 * torch.sin(2 * torch.pi * 0.5 * t)
# ----------------------------------

def main():
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    sim.set_camera_view([3, 0, 2], [0, 0, 0.5])

    scene_cfg = Xarm6SceneCfg(num_envs=args_cli.num_envs, env_spacing=1.5)
    scene = InteractiveScene(scene_cfg)

    sim.reset()
    print(f"[INFO] Scene ready with {args_cli.num_envs} robots")

    run_sim(sim, scene)


if __name__ == "__main__":
    main()
    simulation_app.close()
