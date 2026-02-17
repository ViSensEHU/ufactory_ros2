from omni.isaac.core import World
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.prims import get_prim_at_path

# 1. Conectarse al mundo ya en ejecución
world = World()

# 2. Cargar el robot como Articulation
robot = Articulation("/UF_ROBOT")

# 3. PRIM PATH de la joint del sensor (la que conecta con el robot)
sensor_joint_prim_path = "/UF_ROBOT/TorqSensor/root_joint"

# 4. Obtener el nombre de la joint a partir del prim path
sensor_joint_prim = get_prim_at_path(sensor_joint_prim_path)
sensor_joint_name = sensor_joint_prim.GetName()
print("Nombre de la joint del sensor:", sensor_joint_name)

# 5. Obtener metadata de joints del ArticulationView
metadata = robot._articulation_view._metadata
joint_indices = metadata.joint_indices   # dict: nombre → índice

# 6. Índice de la joint del sensor
sensor_joint_index = joint_indices[sensor_joint_name]

# 7. Fila real en get_measured_joint_forces()
row_index = sensor_joint_index + 1

print("Índice interno de la joint:", sensor_joint_index)
print("Fila en get_measured_joint_forces():", row_index)

forces = robot.get_measured_joint_forces()  # shape: (num_joints+1, 6)
ft = forces[row_index]                      # [Fx, Fy, Fz, Tx, Ty, Tz]
print("F/T sensor:", ft)

