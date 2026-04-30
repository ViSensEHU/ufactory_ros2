import math
from isaaclab.utils import configclass

import isaaclab_tasks.manager_based.manipulation.reach.mdp as mdp
from isaaclab_tasks.manager_based.manipulation.reach.reach_env_cfg import ReachEnvCfg

from .xarm6_config import XARM6_CONFIG


@configclass
class Xarm6ReachEnvCfg(ReachEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # 1. Asignar tu robot
        self.scene.robot = XARM6_CONFIG.replace(prim_path="{ENV_REGEX_NS}/Robot")

        # 2. Definir el end-effector
        # Debes poner aquí el nombre EXACTO del link final en tu USD
        ee_name = "xarm_gripper_base_link"   # <-- cámbialo si tu USD usa otro nombre

        # 3. Ajustar recompensas para tu end-effector
        self.rewards.end_effector_position_tracking.params["asset_cfg"].body_names = [ee_name]
        self.rewards.end_effector_position_tracking_fine_grained.params["asset_cfg"].body_names = [ee_name]
        self.rewards.end_effector_orientation_tracking.params["asset_cfg"].body_names = [ee_name]

        # 4. Definir las articulaciones controladas
        # Usa expresiones regulares si tus joints se llaman joint1, joint2, ...
        self.actions.arm_action = mdp.JointPositionActionCfg(
            asset_name="robot",
            #joint_names=["joint.*", "Component2_to_BaseLink"],   # <-- controla todas las articulaciones
            joint_names=["joint.*"],
            scale=0.5,
            use_default_offset=True
        )

        # 5. Ajustar el generador de comandos (objetivo de reaching)
        self.commands.ee_pose.body_name = ee_name

        # Rango de posiciones donde quieres que aparezca el objetivo
        #self.commands.ee_pose.ranges.pos_x = (0.2, 0.6)
        #self.commands.ee_pose.ranges.pos_y = (-0.3, 0.3)
        #self.commands.ee_pose.ranges.pos_z = (0.1, 0.5)

        # 6. Ajustar orientación del end-effector
        # Si tu herramienta apunta en +Z, usa esto:
        self.commands.ee_pose.ranges.pitch = (math.pi, math.pi)


@configclass
class Xarm6ReachEnvCfg_PLAY(Xarm6ReachEnvCfg):
    def __post_init__(self):
        super().__post_init__()

        # Modo "play"
        self.scene.num_envs = 10
        self.scene.env_spacing = 2.0

        # Sin ruido en observaciones
        self.observations.policy.enable_corruption = False
