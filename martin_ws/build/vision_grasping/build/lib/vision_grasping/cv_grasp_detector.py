"""
cv_grasp_detector.py (Optimizado con Ángulo de Rotación por Momentos y Centro de Masas)
======================================================================================
Sustituye completamente al detector de círculos rígido. 
Calcula el Centro de Masas, el diámetro para la apertura y la orientación angular 
óptima de la pinza basándose en la geometría del contorno.
"""

import cv2
import threading
import numpy as np

# ---------------------------------------------------------------------------
# Parámetros de detección — Ajustados para el entorno de las pelotas
# ---------------------------------------------------------------------------

# Color objetivo: 'green' | 'red' | 'blue' | 'yellow' | 'pink' | 'brown' | 'custom'
TARGET_COLOR = 'green'

# Rango HSV personalizado (solo si TARGET_COLOR = 'custom')
HSV_LOWER_CUSTOM = np.array([35,  60,  60])
HSV_UPPER_CUSTOM = np.array([85, 255, 255])

# Filtros de tamaño del objeto (Área en píxeles del contorno)
# Reducido el mínimo para evitar descartes por sombras o distancias altas
OBJECT_AREA_MIN_PX = 150   
OBJECT_AREA_MAX_PX = 50000 

# Umbral de circularidad permisivo (0.0 a 1.0)
# Un valor de 0.75 permite tolerar pelotas muy ladeadas (óvalos por perspectiva) o bordes con sombras
CIRCULARITY_MIN = 0.73
ASPECT_RATIO_MAX = 1.26  # ratio eje_mayor/eje_menor máximo permitido
                          # pelota ≈ 1.0-1.1, cuadrado ≈ 1.3-1.5

# Rango de profundidad válida en milimetros (para descartar ruido y objetos demasiado cercanos/lejanos)
DEPTH_VALID_MIN = 10.0   # 10 mm (1 cm)
DEPTH_VALID_MAX = 1200.0 # 1200 mm (1.2 metros)

# Apertura de garra proporcional al tamaño detectado (escala píxeles)
GRIPPER_WIDTH_FACTOR = 1.4
GRIPPER_WIDTH_MAX    = 140

# Rangos HSV predefinidos por color
_HSV_RANGES = {
    'green':  (np.array([35,   60,  60]), np.array([85,  255, 255])),
    'blue':   (np.array([100,  80,  50]), np.array([130, 255, 255])),
    'yellow': (np.array([ 20,  80,  80]), np.array([ 35, 255, 255])),
    'pink':   (np.array([140,  60,  80]), np.array([170, 255, 255])),
    'brown':  (np.array([5,   80,  40]), np.array([20, 200, 150])),
}

# Colores de visualización BGR
_VIS_VALID   = (  0, 255,   0)   # verde  — contorno válido
_VIS_INVALID = (  0,   0, 255)   # rojo   — descartado
_VIS_GRASP   = (  0, 255, 255)   # amarillo — objetivo y ángulo calculado


class CVGraspDetector:
    def __init__(self, ggcnn_config, depth_img_que, ggcnn_cmd_que):
        self.depth_img_que    = depth_img_que
        self.ggcnn_cmd_que    = ggcnn_cmd_que
        self.open_loop_height = ggcnn_config['OPEN_LOOP_HEIGHT'] / 1000.0
        self.depth_cam_k      = ggcnn_config['DEPTH_CAM_K']
        self.grasp_img        = None
        self._color_img       = None
        self._prev_center     = None   # (cx, cy) para continuidad temporal

        if ggcnn_config.get('GGCNN_IN_THREAD', False):
            threading.Thread(target=self._run_loop, daemon=True).start()

    def _run_loop(self):
        while True:
            data = self.depth_img_que.get()
            robot_pos, depth = data[0], data[1]
            self.grasp_img, result = self.get_grasp_img(
                depth, self.depth_cam_k, robot_pos[2])
            if result:
                if not self.ggcnn_cmd_que.empty():
                    self.ggcnn_cmd_que.get()
                self.ggcnn_cmd_que.put([robot_pos, result])

    def get_grasp_img(self, depth_image, depth_cam_k, robot_z):
        if self._color_img is None:
            return self._vis_empty(depth_image), None

        color_img = self._color_img
        H, W = color_img.shape[:2]

        if depth_image.shape[:2] != (H, W):
            depth_image = cv2.resize(
                depth_image, (W, H), interpolation=cv2.INTER_NEAREST)

        fx, fy = depth_cam_k[0, 0], depth_cam_k[1, 1]
        cx, cy = depth_cam_k[0, 2], depth_cam_k[1, 2]

        # 1. Máscara de color HSV + Filtros morfológicos
        color_mask = self._color_mask(color_img)

        # 2. Segmentación de contornos
        contours, _ = cv2.findContours(color_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        valid_objects = []
        invalid_contours = []

        for cnt in contours:
            area = cv2.contourArea(cnt)
            if not (OBJECT_AREA_MIN_PX <= area <= OBJECT_AREA_MAX_PX):
                invalid_contours.append(cnt)
                continue

            perimeter = cv2.arcLength(cnt, True)
            if perimeter == 0:
                continue
            
            # Filtro de circularidad
            circularity = (4 * np.pi * area) / (perimeter ** 2)

            if circularity >= CIRCULARITY_MIN:
                # Verificar relación de aspecto — descarta cuadrados y rectángulos
                if len(cnt) >= 5:
                    ellipse = cv2.fitEllipse(cnt)
                    minor_axis = min(ellipse[1])
                    major_axis = max(ellipse[1])
                    aspect_ratio = major_axis / max(minor_axis, 1)
                    if aspect_ratio > ASPECT_RATIO_MAX:
                        invalid_contours.append(cnt)
                        continue

                M = cv2.moments(cnt)
                if M["m00"] == 0:
                    continue
                cX = int(M["m10"] / M["m00"])
                cY = int(M["m01"] / M["m00"])
                
                # --- CÁLCULO DEL ÁNGULO ÓPTIMO POR MOMENTOS CENTRALES ---
                # Idéntico concepto matemático que el arctan2 de GG-CNN, pero sobre el contorno.
                # Evaluamos la orientación del eje de inercia principal.
                mu11 = M["mu11"]
                mu20 = M["mu20"]
                mu02 = M["mu02"]
                
                # Ángulo del contorno en radianes (-pi/2 a pi/2)
                angle_rad = 0.5 * np.arctan2(2 * mu11, mu20 - mu02)
                
                # Ajuste de orientación: la pinza se orienta según el eje largo del objeto
                angle_grasp = angle_rad
                if angle_grasp > np.pi / 2:
                    angle_grasp += np.pi
                elif angle_grasp < -np.pi / 2:
                    angle_grasp -= np.pi

                # Estimación del radio equivalente
                equiv_radius = int(np.sqrt(area / np.pi))
                valid_objects.append((cX, cY, equiv_radius, angle_grasp, cnt))
            else:
                invalid_contours.append(cnt)

        if not valid_objects:
            return self._vis(depth_image, invalid_contours, [], None, color_mask), None

        # 3. Selección temporal del mejor candidato
        best = self._select(valid_objects)
        cx_b, cy_b, r_b, ang_b, best_cnt = best
        self._prev_center = (cx_b, cy_b)

        # 4. Extracción de profundidad robusta en el Centro de Masas
        pad = max(2, min(r_b // 3, 15))
        patch = depth_image[
            max(0, cy_b - pad):min(H, cy_b + pad),
            max(0, cx_b - pad):min(W, cx_b + pad)
        ].flatten()
        patch = patch[~np.isnan(patch)]
        patch = patch[(patch > DEPTH_VALID_MIN) & (patch < DEPTH_VALID_MAX)]

        if len(patch) == 0:
            return self._vis(depth_image, invalid_contours, valid_objects, None, color_mask), None

        patch.sort()
        z = float(patch[:max(1, len(patch) // 3)].mean())

        # 5. Proyección Píxel -> Coordenadas 3D (Marco de la Cámara)
        x_cam = (cx_b - cx) / fx * z
        y_cam = (cy_b - cy) / fy * z

        # 6. Apertura dinámica de la pinza usando el bounding box real orientado
        _, _, w_box, _ = cv2.boundingRect(best_cnt)
        width_px = float(np.clip(w_box * GRIPPER_WIDTH_FACTOR, 0, GRIPPER_WIDTH_MAX))

        # 7. Centro de profundidad para control de colisiones en milímetros
        rc, cc = H // 2, W // 2
        cp = depth_image[rc-20:rc+20, cc-20:cc+20].flatten()
        cp = cp[~np.isnan(cp)]
        cp.sort()
        depth_center = float(cp[:10].mean()) * 1000.0 if len(cp) >= 10 else 0.0

        grasp_img = self._vis(depth_image, invalid_contours, valid_objects, best, color_mask)
        
        # RETORNA EL ÁNGULO DINÁMICO EN LUGAR DE 0.0
        return grasp_img, {
            "x": float(x_cam),
            "y": float(y_cam),
            "z": float(z),
            "angle": float(ang_b),
            "width_px": float(width_px),
            "depth_center": float(depth_center),
            "center": (float(cx_b), float(cy_b)),
            "quality": float(1.0)  # Métrica fija de calidad para el logger de app.py
        }

    def _color_mask(self, color_img):
        hsv = cv2.cvtColor(color_img, cv2.COLOR_BGR2HSV)
        if TARGET_COLOR == 'custom':
            mask = cv2.inRange(hsv, HSV_LOWER_CUSTOM, HSV_UPPER_CUSTOM)
        elif TARGET_COLOR == 'red':
            m1 = cv2.inRange(hsv, np.array([  0, 80, 80]), np.array([ 10, 255, 255]))
            m2 = cv2.inRange(hsv, np.array([170, 80, 80]), np.array([180, 255, 255]))
            mask = cv2.add(m1, m2)
        else:
            lo, hi = _HSV_RANGES.get(TARGET_COLOR, _HSV_RANGES['green'])
            mask = cv2.inRange(hsv, lo, hi)
        
        k = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
        mask = cv2.morphologyEx(mask, cv2.MORPH_OPEN,  k, iterations=2)
        mask = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, k, iterations=2)
        return mask

    def _select(self, objects):
        if self._prev_center is None:
            return max(objects, key=lambda o: o[2])
        def dist(o):
            return (o[0] - self._prev_center[0])**2 + (o[1] - self._prev_center[1])**2
        return min(objects, key=dist)

    def _vis_empty(self, depth_image):
        return self._vis(depth_image, [], [], None, None)

    def _vis(self, depth_image, invalid_cnts, valid_objs, best_obj, color_mask):
        H, W = depth_image.shape[:2]
        d = np.nan_to_num(depth_image, nan=0)
        vp = d[d > 0]
        dmin, dmax = (vp.min(), vp.max()) if len(vp) else (0, 1)
        norm = ((d - dmin) / max(dmax - dmin, 1e-6) * 255).astype(np.uint8)
        vis  = cv2.applyColorMap(norm, cv2.COLORMAP_BONE)

        if color_mask is not None:
            ov = vis.copy()
            ov[color_mask > 0] = [0, 60, 0]
            vis = cv2.addWeighted(vis, 0.8, ov, 0.2, 0)

        # Pintar descartados en rojo
        cv2.drawContours(vis, invalid_cnts, -1, _VIS_INVALID, 1)

        # Pintar válidos en verde
        for (cx, cy, r, ang, cnt) in valid_objs:
            if best_obj and (cx, cy) == (best_obj[0], best_obj[1]):
                continue
            cv2.drawContours(vis, [cnt], -1, _VIS_VALID, 2)

        # Resaltar en Amarillo el Target y dibujar vector de la orientación de la pinza
        if best_obj:
            cx_b, cy_b, r_b, ang_b, cnt_b = best_obj
            cv2.drawContours(vis, [cnt_b], -1, _VIS_GRASP, 2)
            cv2.circle(vis, (cx_b, cy_b), 4, _VIS_GRASP, -1)
            
            # Dibujar la línea de orientación de la garra (Eje del Grasp)
            # Calculamos los puntos extremos de una línea que cruza el centro con el ángulo ang_b
            length = max(30, r_b + 10)
            x1 = int(cx_b - length * np.cos(ang_b))
            y1 = int(cy_b - length * np.sin(ang_b))
            x2 = int(cx_b + length * np.cos(ang_b))
            y2 = int(cy_b + length * np.sin(ang_b))
            
            # Línea de agarre principal
            cv2.line(vis, (x1, y1), (x2, y2), _VIS_GRASP, 2)
            # Topes visuales perpendiculares (simulando los dedos de la garra)
            for x_c, y_c in [(x1, y1), (x2, y2)]:
                tx1 = int(x_c - 10 * np.sin(ang_b))
                ty1 = int(y_c + 10 * np.cos(ang_b))
                tx2 = int(x_c + 10 * np.sin(ang_b))
                ty2 = int(y_c - 10 * np.cos(ang_b))
                cv2.line(vis, (tx1, ty1), (tx2, ty2), _VIS_GRASP, 2)

            deg = int(np.degrees(ang_b))
            cv2.putText(vis, f'Grasp Ang: {deg}deg', (cx_b + r_b + 10, cy_b),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.45, _VIS_GRASP, 1)
        return vis