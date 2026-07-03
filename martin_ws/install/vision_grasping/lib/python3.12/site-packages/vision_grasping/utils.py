import numpy as np

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
