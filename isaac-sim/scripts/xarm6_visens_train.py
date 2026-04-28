import argparse
from isaaclab.app import AppLauncher

# Argumentos en la CLI (Command Line Interface)
parser = argparse.ArgumentParser()
parser.add_argument("--num_envs", type=int, default=32)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# Ejecutar Isaac Sim
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
    init_state=ArticulationCfg.InitialStateCfg( # Posiciones iniciales
        pos=(0.0, 0.0, 0.05),                   # Motor lineal completamente sobre el plano
        rot=(0.7071068, 0.7071068, 0.0, 0.0),   # Rotación del conjunto
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
            stiffness=None,                     #73.29828, # None --> valor del USD.
            damping=None,                       #0.02932,
        ),
        "joint2": ImplicitActuatorCfg(
            joint_names_expr=["joint2"],
            stiffness=None,                     #114.32549,
            damping=None,                       #0.04573,
        ),
        "joint3": ImplicitActuatorCfg(
            joint_names_expr=["joint3"],
            stiffness=None,                     #95.28044,
            damping=None,                       #0.03811,
        ),
        "joint4": ImplicitActuatorCfg(
            joint_names_expr=["joint4"],
            stiffness=None,                     #283.06,
            damping=None,                       #0.11322,
        ),
        "joint5": ImplicitActuatorCfg(
            joint_names_expr=["joint5"],
            stiffness=None,                     #9.7635,
            damping=None,                       #0.00391,
        ),
        "joint6": ImplicitActuatorCfg(
            joint_names_expr=["joint6"],
            stiffness=None,                     #2.07821,
            damping=None,                       #0.00083,
        ),
        "drive_joint": ImplicitActuatorCfg(
            joint_names_expr=["drive_joint"],
            stiffness=None,                     #0.54539,
            damping=None,                       #0.00022,
        ),
        "linear_motor": ImplicitActuatorCfg(
            joint_names_expr=["Component2_to_BaseLink"],
            stiffness=None,                     #16000.0,
            damping=None,                       #2800.0,
        ),
    }
)
# -------------------------------


# --- Configuración de la escena ---
@configclass
class Xarm6VisensSceneCfg(InteractiveSceneCfg):
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
            #print("[INFO] Resetting robots")
            print("[INFO] Robotak berrasieratzen...")
            count = 0

            # Reset del estado raíz (root): posición, orientación, velocidades 
            # default_root_state viene de la configuración inicial del robot: líneas 36-37
            root = scene["robot"].data.default_root_state.clone()
            root[:, :3] += scene.env_origins
            scene["robot"].write_root_pose_to_sim(root[:, :7])
            scene["robot"].write_root_velocity_to_sim(root[:, 7:])

            # Reset de las articulaciones: posiciones y velocidades iniciales
            # default_joint viene de la configuración inicial del robot: líneas 38-46
            jpos = scene["robot"].data.default_joint_pos.clone()
            jvel = scene["robot"].data.default_joint_vel.clone()
            scene["robot"].write_joint_state_to_sim(jpos, jvel)

            # Reset interno de buffers, sensores y PhysX
            scene.reset()

        # Obtener nombres e índices de las articulaciones del robot
        joint_names = scene["robot"].joint_names 
        joint_indices = list(range(len(joint_names)))
        joint_idx_map = {name: idx for idx, name in enumerate(joint_names)}

        # Crear el vector de posiciones objetivo para las articulaciones
        target_pos = scene["robot"].data.default_joint_pos.clone()
        target_pos[:, joint_idx_map["joint1"]] = 0.4
        target_pos[:, joint_idx_map["joint2"]] = 0.0
        target_pos[:, joint_idx_map["joint3"]] = -0.5
        target_pos[:, joint_idx_map["joint4"]] = 0.0
        target_pos[:, joint_idx_map["joint5"]] = 0.0
        target_pos[:, joint_idx_map["joint6"]] = 0.0
        target_pos[:, joint_idx_map["drive_joint"]] = 0.5
        target_pos[:, joint_idx_map["Component2_to_BaseLink"]] = 0.3

        # Enviar los objetivos articulares al controlador del robot
        scene["robot"].set_joint_position_target(target_pos)

        # Escribir los datos en la simulación (PhysX)
        scene.write_data_to_sim()

        # Avanzar un paso de la simulación
        sim.step()

        # Actualizar buffers y sensores de la escena
        scene.update(sim_dt)
        sim_time += sim_dt
        count += 1
# ----------------------------------

def main():
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    sim.set_camera_view([3, 0, 2], [0, 0, 0.5])

    scene_cfg = Xarm6VisensSceneCfg(num_envs=args_cli.num_envs, env_spacing=1.5)
    scene = InteractiveScene(scene_cfg)

    sim.reset()
    #print(f"[INFO] Escena cargada with {args_cli.num_envs} robots")
    print(f"[INFO] {args_cli.num_envs} robotez kargatutako eszena")

    run_sim(sim, scene)


if __name__ == "__main__":
    main()
    simulation_app.close()
