"""
Modo PLAY para el entorno de reaching del xArm6.
"""

import argparse
from isaaclab.app import AppLauncher

# Argumentos CLI
parser = argparse.ArgumentParser(description="PLAY mode for xArm6 reaching task.")
parser.add_argument("--num_envs", type=int, default=10)
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# Lanzar Isaac Sim
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# ---------------------------------------------------------------------------

import torch
from isaaclab.envs import ManagerBasedRLEnv
from xarm6_reach_env_cfg import Xarm6ReachEnvCfg_PLAY


def main():
    # Crear configuración del entorno
    env_cfg = Xarm6ReachEnvCfg_PLAY()
    env_cfg.scene.num_envs = args_cli.num_envs
    env_cfg.sim.device = args_cli.device

    # Crear entorno RL
    env = ManagerBasedRLEnv(cfg=env_cfg)

    # Reset inicial
    obs, _ = env.reset()

    print("[INFO] PLAY mode iniciado. Observa la simulación.")

    count = 0
    while simulation_app.is_running():
        with torch.inference_mode():
            # Acción aleatoria para ver movimiento
            action = torch.randn_like(env.action_manager.action)

            obs, rew, terminated, truncated, info = env.step(action)

            if terminated.any() or truncated.any():
                print("[INFO] Reset...")
                obs, _ = env.reset()

            count += 1

    env.close()


if __name__ == "__main__":
    main()
    simulation_app.close()
