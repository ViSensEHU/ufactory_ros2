import numpy as np
import math
from .helpers.matrix_funcs import euler2mat, convert_pose

def compute_crop_and_intrinsics(depth_image, depth_cam_k):
    """
    Calcula:
      - crop_size
      - crop_x_inx, crop_y_inx
      - DEPTH_CAM_K_CROP (intrínsecas corregidas)
    """

    imh, imw = depth_image.shape
    crop_size  = min(imh, imw)
    crop_y_inx = max(0, imh - crop_size) // 2
    crop_x_inx = max(0, imw - crop_size) // 2

    # Corregir intrínsecas
    depth_cam_k_crop = depth_cam_k.copy()
    depth_cam_k_crop[0, 2] -= crop_x_inx
    depth_cam_k_crop[1, 2] -= crop_y_inx

    return crop_size, crop_x_inx, crop_y_inx, depth_cam_k_crop

def get_combined_img(img, grasp_img):    
    img_shape =  img.shape
    grasp_shape = grasp_img.shape

    img = np.nan_to_num(img, nan=0)
    grasp_img = np.nan_to_num(grasp_img, nan=0)

    if len(img_shape) != 3:
        img = cv2.applyColorMap((img * 255).astype(np.uint8), cv2.COLORMAP_BONE)

    if len(grasp_shape) != 3:
        grasp_img = cv2.applyColorMap((grasp_img * 255).astype(np.uint8), cv2.COLORMAP_HOT)

    combined_img = np.zeros((img_shape[0], img_shape[1] + grasp_shape[1] + 10, 3), np.uint8)
    combined_img[:img_shape[0], :img_shape[1]] = img
    combined_img[:grasp_img.shape[0], img_shape[1]+10:img_shape[1]+grasp_shape[1]+10] = grasp_img

    return combined_img

def compute_goal_pose(result,
                      eef_pose,
                      euler_eef_to_color_opt,
                      euler_color_to_depth_opt,
                      gripper_z_mm,
                      grasping_min_z,
                      grasping_range,
                      min_result_z):
    """
    Replica la parte matemática del método RobotGrasp.grasp(),
    devolviendo únicamente GOAL_POS para ROS2.
    """

    # result = (x, y, z, angle)
    d = [result.x, result.y, result.z, result.angle]

    # Si la profundidad es demasiado baja, no es válido
    if d[2] <= min_result_z:
        return None

    # 1. Pose del grasp en el frame de la cámara de profundidad
    gp = [d[0], d[1], d[2], 0, 0, -d[3]]  # xyzrpy en metros

    # 2. Transformación depthOpt → base
    mat_depthOpt_in_base = (
        euler2mat(eef_pose) *
        euler2mat(euler_eef_to_color_opt) *
        euler2mat(euler_color_to_depth_opt)
    )

    gp_base = convert_pose(gp, mat_depthOpt_in_base)

    # 3. Corregir yaw
    if gp_base[5] < -np.pi:
        gp_base[5] += np.pi
    elif gp_base[5] > 0:
        gp_base[5] -= np.pi

    # 4. Construir GOAL_POS
    x_mm = gp_base[0] * 1000
    y_mm = gp_base[1] * 1000
    z_mm = gp_base[2] * 1000 + gripper_z_mm

    roll = 180
    pitch = 0
    yaw = math.degrees(gp_base[5] + np.pi)

    # 5. Validar altura mínima
    if z_mm < grasping_min_z:
        z_mm = grasping_min_z

    # 6. Validar rango
    if x_mm < grasping_range[0] or x_mm > grasping_range[1] or \
       y_mm < grasping_range[2] or y_mm > grasping_range[3]:
        return None

    return [x_mm, y_mm, z_mm, roll, pitch, yaw]
