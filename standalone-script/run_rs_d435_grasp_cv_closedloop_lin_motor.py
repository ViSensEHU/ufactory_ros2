"""
run_rs_d435_grasp_cv_closedloop.py
===================================
Orquestador principal. Responsabilidades:
  - Capturar frames de la RealSense D435 (hilo dedicado)
  - Recortar y pasar imágenes al CVGraspDetector
  - Poner resultados en la cola → robot_grasp.py se encarga del resto
"""

import os
import sys
import cv2
import time
import threading
import numpy as np
from queue import Queue

sys.path.append(os.path.join(os.path.dirname(__file__), '../..'))
from camera.rs_camera import RealSenseCamera
from camera.utils import get_combined_img
from grasp.cv_grasp_detector import CVGraspDetector
from grasp.robot_grasp_lin_motor import RobotGrasp

# ---------------------------------------------------------------------------
# Configuración
# ---------------------------------------------------------------------------

WIN_NAME   = 'RealSense-D435'
CAM_WIDTH  = 640
CAM_HEIGHT = 480

# use open-loop solution when robot height is over OPEN_LOOP_HEIGHT
OPEN_LOOP_HEIGHT = 340   # mm
GGCNN_IN_THREAD  = False

# show the grasp image of ggcnn or not, otherwise show native depth images.
SHOW_GRASP_IMG   = True

# rgb camera calibration result
EULER_EEF_TO_COLOR_OPT   = [0.067052239, -0.0311387575, 0.021611456, -0.004202176, -0.00848499, 1.5898775]
EULER_COLOR_TO_DEPTH_OPT = [0.015, 0, 0, 0, 0, 0]

# The range of motion of the robot grasping
# If it exceeds the range, it will return to the initial detection position.
GRASPING_RANGE = [-180, 650, -480, 480] # [x_min, x_max, y_min, y_max]

# initial detection position
DETECT_XYZ     = [220.5, 0, 575] # [x, y, z]

# release grasping pos
RELEASE_XYZ    = [0, 360.5, 488] # [x, y, z]

# lift offset based on DETECT_XYZ[2] after grasping or release
LIFT_OFFSET_Z  = 0 # lift_height = DETECT_XYZ[2] + LIFT_OFFSET_Z

# The distance between the gripping point of the robot grasping and the end of the robot arm flange
# The value needs to be fine-tuned according to the actual situation.
GRIPPER_Z_MM   = 150

# minimum z for grasping
GRASPING_MIN_Z = 0

# ---------------------------------------------------------------------------
# Hilo de captura — evita que el buffer de la RealSense expire
# ---------------------------------------------------------------------------

class CameraThread(threading.Thread):
    def __init__(self, camera):
        super().__init__(daemon=True)
        self.camera = camera
        self.latest_color = None
        self.latest_depth = None
        self._lock = threading.Lock()
        self._stop = threading.Event()

    def run(self):
        while not self._stop.is_set():
            try:
                color, depth = self.camera.get_images(align=True)
                with self._lock:
                    self.latest_color = color
                    self.latest_depth = depth
            except Exception as e:
                print(f'[CameraThread] {e}')
                time.sleep(0.005)

    def get_latest(self):
        with self._lock:
            return self.latest_color, self.latest_depth

    def stop(self):
        self._stop.set()


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------

def main():
    if len(sys.argv) < 2:
        print('Usage: {} <robot_ip>'.format(sys.argv[0]))
        exit(1)

    robot_ip = sys.argv[1]

    depth_img_que = Queue(1)
    ggcv_cmd_que = Queue(1)

    # --- Cámara ---
    camera = RealSenseCamera(width=CAM_WIDTH, height=CAM_HEIGHT, serial_number='231122070195')
    color_intrin, _ = camera.get_intrinsics(align=True)

    DEPTH_CAM_K = np.array([
        [color_intrin.fx, 0,               color_intrin.ppx],
        [0,               color_intrin.fy,  color_intrin.ppy],
        [0,               0,               1               ]
    ])

    # Arrancar hilo de cámara antes de cualquier otra inicialización
    cam_thread = CameraThread(camera)
    cam_thread.start()

    print('[INIT] Esperando primer frame...')
    t0 = time.time()
    while True:
        color_image, depth_image = cam_thread.get_latest()
        if color_image is not None and depth_image is not None:
            print('[INIT] Cámara lista.')
            break
        if time.time() - t0 > 10:
            print('[ERROR] Sin frames tras 10s. Revisar conexión USB.')
            cam_thread.stop()
            camera.stop()
            return
        time.sleep(0.05)

    # --- Índices de crop y corrección de intrínsecos ---
    imh, imw  = depth_image.shape
    crop_size  = min(imh, imw)
    crop_y_inx = max(0, imh - crop_size) // 2
    crop_x_inx = max(0, imw - crop_size) // 2

    # Al recortar, el punto principal se desplaza → corregir cx, cy
    DEPTH_CAM_K_CROP = DEPTH_CAM_K.copy()
    DEPTH_CAM_K_CROP[0, 2] -= crop_x_inx
    DEPTH_CAM_K_CROP[1, 2] -= crop_y_inx

    # --- Detector ---
    detector_config = {
        'OPEN_LOOP_HEIGHT': OPEN_LOOP_HEIGHT,
        'GGCNN_IN_THREAD':  GGCNN_IN_THREAD,
        'DEPTH_CAM_K':      DEPTH_CAM_K_CROP,
    }
    gg_cv = CVGraspDetector(detector_config, depth_img_que, ggcv_cmd_que)
    time.sleep(2)

    # --- Robot ---
    euler_opt = {
            'EULER_EEF_TO_COLOR_OPT':   EULER_EEF_TO_COLOR_OPT,
            'EULER_COLOR_TO_DEPTH_OPT': EULER_COLOR_TO_DEPTH_OPT,
    }
    grasp_config = {
        'GRASPING_RANGE':  GRASPING_RANGE,
        'DETECT_XYZ':      DETECT_XYZ,
        'RELEASE_XYZ':     RELEASE_XYZ,
        'LIFT_OFFSET_Z':   LIFT_OFFSET_Z,
        'GRIPPER_Z_MM':    GRIPPER_Z_MM,
        'GRASPING_MIN_Z':  GRASPING_MIN_Z,
        'MIN_RESULT_Z_MM': 250,
    }

    """grasp = RobotGrasp(
        robot_ip,
        ggcv_cmd_que,
        euler_opt,
        grasp_config
    )"""

    last_cmd_time = 0.0
    CMD_INTERVAL  = 0.05   # 0.05   segundos entre comandos (~20fps, igual que GG-CNN)

    # --- Bucle principal ---
    while True: #grasp.is_alive():

        color_image, depth_image = cam_thread.get_latest()
        if color_image is None or depth_image is None:
            time.sleep(0.005)
            continue

        # Recortar color y depth al mismo ROI cuadrado
        color_crop = color_image[crop_y_inx:crop_y_inx + crop_size,
                                 crop_x_inx:crop_x_inx + crop_size, :]
        depth_crop = depth_image[crop_y_inx:crop_y_inx + crop_size,
                                 crop_x_inx:crop_x_inx + crop_size]

        gg_cv._color_img = color_crop
        #robot_pos = grasp.get_eef_pose_m()
        robot_pos = [220.5, 0, 650, 180, 0, 0]

        if GGCNN_IN_THREAD:
            if not depth_img_que.empty():
                depth_img_que.get()
            depth_img_que.put([robot_pos, depth_crop])
            grasp_img = gg_cv.grasp_img or depth_crop
        else:
            grasp_img, result = gg_cv.get_grasp_img(
                depth_crop, DEPTH_CAM_K_CROP, robot_pos[2])

            if result:
                now = time.monotonic()
                if now - last_cmd_time >= CMD_INTERVAL:
                    if not ggcv_cmd_que.empty():
                        ggcv_cmd_que.get()
                    ggcv_cmd_que.put([robot_pos, result])
                    last_cmd_time = now

            if not SHOW_GRASP_IMG or grasp_img is None:
                grasp_img = depth_crop

        cv2.imshow(WIN_NAME, get_combined_img(color_crop, grasp_img))

        key = cv2.waitKey(1)
        if key & 0xFF == ord('q') or key == 27:
            break

    cam_thread.stop()
    camera.stop()
    cv2.destroyAllWindows()


if __name__ == '__main__':
    main()
