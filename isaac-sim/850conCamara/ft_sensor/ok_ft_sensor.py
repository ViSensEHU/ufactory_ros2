import omni.isaac.core.utils.prims as prim_utils
from isaacsim.core.prims import Articulation
from omni.isaac.core.utils.prims import get_prim_at_path

def compute(db: og.Database):
    # Get your articulation
    articulation = Articulation(prim_path="/UF_ROBOT/ft_sensor/FixedJoint")
    
    # CHECK: Is physics handle valid before accessing?
    if not articulation.is_physics_handle_valid():
        db.log_info("AAAAAAAAAAAA")
        # Physics not ready yet - skip this frame
        return
    
    # CHECK: Is articulation view initialized?
    if articulation._articulation_view is None:
        return
        
    # Now safe to access physics data
    try:
        joint_forces = articulation.get_measured_joint_forces()
        fx, fy, fz, tx, ty, tz = joint_forces[db.state.row_index]
        db.outputs.Fx = fx
        db.outputs.Fy = fy
        db.outputs.Fz = fz
        db.outputs.Tx = tx
        db.outputs.Ty = ty
        db.outputs.Tz = tz
    except Exception as e:
        # Handle any remaining edge cases
        return
