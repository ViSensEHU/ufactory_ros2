import omni.graph.core as og
from omni.isaac.core.articulations import Articulation
from omni.isaac.core.utils.prims import get_prim_at_path

def setup(db: og.Database):
    # Crear el articulation del robot
    db.state.robot = Articulation("/World/xarm6")

    # Joint del sensor
    # sensor_joint_prim_path = "/UF_ROBOT/TorqSensor/ft_sensor_root_joint"
    sensor_joint_prim_path = "/World/JoinedTorqueSensor/FixedJoint_TorqueSensor_Link6"
    sensor_joint_prim = get_prim_at_path(sensor_joint_prim_path)
    sensor_joint_name = sensor_joint_prim.GetName()

    # Metadata del articulation
    metadata = db.state.robot._articulation_view._metadata
    joint_indices = metadata.joint_indices
    joint_names = metadata.joint_names

    # Índice interno de la joint
    sensor_joint_index = joint_indices[sensor_joint_name]

    print("Joint indices: ", joint_indices)
    print("Joint names: ", joint_names)
    print("sensor_joint_prim_path: ", sensor_joint_prim_path)
    print("sensor_joint_name: ", sensor_joint_name)
    print("sensor_joint_index: ", sensor_joint_index)

    # Fila real en get_measured_joint_forces()
    db.state.row_index = sensor_joint_index + 1

    db.log_info(f"F/T sensor joint: {sensor_joint_name}, row index: {db.state.row_index}")

    # db.state.initialized = True

def compute(db: og.Database):
    # if not db.state.initialized:
    #    setup(db)
    
    # Leer fuerzas cada frame
    forces = db.state.robot.get_measured_joint_forces()
    fx, fy, fz, tx, ty, tz = forces[db.state.row_index]

    # Output double[6]
    #db.outputs.Forces = [float(fx), float(fy), float(fz),
    #                     float(tx), float(ty), float(tz)]

    db.outputs.Fx = fx
    db.outputs.Fy = fy
    db.outputs.Fz = fz
    db.outputs.Tx = tx
    db.outputs.Ty = ty
    db.outputs.Tz = tz

    return True


def cleanup(db: og.Database):
    db.log_info("F/T Script Node cleaned up")

def cleanup(db: og.Database):
    db.state.robot = None
    db.state.row_index = None
    # db.state.initialized = False
    db.log_info("F/T Script Node cleaned up")

