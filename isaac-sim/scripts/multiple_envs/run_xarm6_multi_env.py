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

USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/scripts/javi_xarm6.usd"

# --- Robot config ---
"""XARM6_CONFIG = ArticulationCfg(
    prim_path="{ENV_REGEX_NS}/Robot",
    spawn=sim_utils.UsdFileCfg(usd_path=USD_PATH),
    init_state=ArticulationCfg.InitialStateCfg(
        pos=(0.0, 0.0, 0.1),
    ),
    actuators={
        "joint1": ImplicitActuatorCfg(
            joint_names_expr=["joint1"],
            stiffness=73.29828,
            damping=0.02932,
        ),
        "joint2": ImplicitActuatorCfg(
            joint_names_expr=["joint2"],
            stiffness=114.32549,
            damping=0.04573,
        ),
        "joint3": ImplicitActuatorCfg(
            joint_names_expr=["joint3"],
            stiffness=95.28044,
            damping=0.03811,
        ),
        "joint4": ImplicitActuatorCfg(
            joint_names_expr=["joint4"],
            stiffness=283.06,
            damping=0.11322,
        ),
        "joint5": ImplicitActuatorCfg(
            joint_names_expr=["joint5"],
            stiffness=9.7635,
            damping=0.00391,
        ),
        "joint6": ImplicitActuatorCfg(
            joint_names_expr=["joint6"],
            effort_limit_sim=20.0,
            stiffness=2.07821,
            damping=0.00083,
        ),
    }
)"""

XARM6_CONFIG = ArticulationCfg(
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
)



# --- Scene config ---
@configclass
class Xarm6SceneCfg(InteractiveSceneCfg):
    ground = AssetBaseCfg(
        prim_path="/World/Ground",
        spawn=sim_utils.GroundPlaneCfg()
    )
    light = AssetBaseCfg(
        prim_path="/World/Light",
        spawn=sim_utils.DomeLightCfg(intensity=3000.0)
    )
    robot = XARM6_CONFIG


def run_sim(sim, scene):
    sim_dt = sim.get_physics_dt()
    sim_time = 0.0
    count = 0

    while simulation_app.is_running():

        if count % 700 == 0:
            print("[INFO] Resetting robots...")
            count = 0

            root = scene["robot"].data.default_root_state.clone()
            root[:, :3] += scene.env_origins
            scene["robot"].write_root_pose_to_sim(root[:, :7])
            scene["robot"].write_root_velocity_to_sim(root[:, 7:])

            jpos = scene["robot"].data.default_joint_pos.clone()
            jvel = scene["robot"].data.default_joint_vel.clone()
            scene["robot"].write_joint_state_to_sim(jpos, jvel)

            scene.reset()

        # ---------------------------------------------------------
        # CONTROL POR POSICIÓN: mover joint1 y joint3
        # ---------------------------------------------------------
        target_pos = scene["robot"].data.default_joint_pos.clone()

        # convertir sim_time → tensor
        t = torch.tensor(sim_time, device=target_pos.device)

        # joint1 → movimiento sinusoidal suave
        target_pos[:, 0] = 0.7854 #1.5708 #0.5 * torch.sin(2 * torch.pi * 0.5 * t)

        target_pos[:, 1] = -0.5236

        target_pos[:, 2] = -0.5236

        # enviar comando
        scene["robot"].set_joint_position_target(target_pos)
        # ---------------------------------------------------------

        scene.write_data_to_sim()
        sim.step()
        scene.update(sim_dt)

        sim_time += sim_dt
        count += 1


def main():
    sim_cfg = sim_utils.SimulationCfg(device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)
    sim.set_camera_view([3, 0, 2], [0, 0, 0.5])

    scene_cfg = Xarm6SceneCfg(num_envs=args_cli.num_envs, env_spacing=2.0)
    scene = InteractiveScene(scene_cfg)

    sim.reset()
    print(f"[INFO] Scene ready with {args_cli.num_envs} robots")

    run_sim(sim, scene)


if __name__ == "__main__":
    main()
    simulation_app.close()
