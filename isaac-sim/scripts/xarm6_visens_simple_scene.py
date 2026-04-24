import argparse
from isaaclab.app import AppLauncher

# Argumentos en la CLI (Command Line Interface)
parser = argparse.ArgumentParser(description="Spawn robot USD into Isaac Sim scene.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# Ejecutar Isaac Sim
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

import isaaclab.sim as sim_utils

from pathlib import Path

# --- Cargar USD ---
# Ruta absoluta
# USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/scripts/usd/xarm6_visens.usd" 

# Ruta relativa
BASE_DIR = Path(__file__).resolve().parent
USD_PATH = str(BASE_DIR / "usd" / "xarm6_visens.usd")
# ------------------

def design_scene():    
    # Plano del suelo
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/GroundPlane", cfg_ground)

    # Luz de la escena
    cfg_light = sim_utils.DistantLightCfg(intensity=3000.0)
    cfg_light.func("/World/Light", cfg_light, translation=(2, 0, 10))

    # USD del robot
    cfg_robot = sim_utils.UsdFileCfg(usd_path=USD_PATH)
    cfg_robot.func("/World/Robot", cfg_robot, translation=(0.0, 0.0, 0.1))

    #print("[INFO] Robot USD loaded at /World/Robot")
    print("[INFO] Robot USD kargatua /World/Robot")


def main():
    # Crear contexto de simulación
    sim_cfg = sim_utils.SimulationCfg(dt=1/60, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)

    # Cámara
    sim.set_camera_view([2.0, 0.0, 2.0], [0.0, 0.0, 0.5])

    # Construir la escena
    design_scene()

    # Resetear simulación
    sim.reset()
    #print("[INFO] Scene ready.")
    print("[INFO] Eszena prest.")

    # Bucle de simulación
    while simulation_app.is_running():
        sim.step()


if __name__ == "__main__":
    main()
    simulation_app.close()
