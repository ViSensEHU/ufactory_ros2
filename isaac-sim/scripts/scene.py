import argparse
from isaaclab.app import AppLauncher

# CLI args
parser = argparse.ArgumentParser(description="Spawn robot USD into Isaac Sim scene.")
AppLauncher.add_app_launcher_args(parser)
args_cli = parser.parse_args()

# Launch Isaac Sim
app_launcher = AppLauncher(args_cli)
simulation_app = app_launcher.app

# ---------------------------------------------------------
# IMPORTS AFTER SIM LAUNCH
# ---------------------------------------------------------
import isaaclab.sim as sim_utils


#USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/xarm6_motorlineal_montaje/instanceOneArtRoot2_xArm6_sensorFuerza_motorLineal.usd"
#USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/scripts/javi_xarm6.usd"

USD_PATH = "/isaac-sim/projects/ufactory_ros2/isaac-sim/xarm6_motorlineal_montaje/instanceNoScript.usd"

def design_scene():
    """Create ground plane + load your robot USD."""
    
    # Ground plane
    cfg_ground = sim_utils.GroundPlaneCfg()
    cfg_ground.func("/World/GroundPlane", cfg_ground)

    # Light
    cfg_light = sim_utils.DistantLightCfg(intensity=3000.0)
    cfg_light.func("/World/Light", cfg_light, translation=(2, 0, 10))

    # Load your USD (robot + motor lineal)
    cfg_robot = sim_utils.UsdFileCfg(usd_path=USD_PATH)
    cfg_robot.func("/World/Robot", cfg_robot, translation=(0.0, 0.0, 0.1))

    print("[INFO] Robot USD loaded at /World/Robot")


def main():
    # Create simulation context
    sim_cfg = sim_utils.SimulationCfg(dt=1/60, device=args_cli.device)
    sim = sim_utils.SimulationContext(sim_cfg)

    # Camera
    sim.set_camera_view([2.0, 0.0, 2.0], [0.0, 0.0, 0.5])

    # Build scene
    design_scene()

    # Reset sim
    sim.reset()
    print("[INFO] Scene ready.")

    # Simulation loop
    while simulation_app.is_running():
        sim.step()


if __name__ == "__main__":
    main()
    simulation_app.close()
