# Reset camera SW
Buscar el puerto de la cámara:
```bash
lsusb
```

Debería salir algo parecido a ``Bus 002 Device 004: ID 8086:0b07 Intel Corp. RealSense D435``.

Para el caso del ejemplo, comprobar que existe la ruta:
```bash
ls -l /dev/bus/usb/002/004
```

Debería salir algo parecido a ``crw-rw-r-- 1 root root 189, 131 jul 23 10:09 /dev/bus/usb/002/004``.

Resetear la cámara:
```bash
sudo usbreset 002/004
```

En Docker, ejecutar el nodo de la cámara:
```bash
ros2 run realsense2_camera realsense2_camera_node --ros-args -p align_depth.enable:=true -p pointcloud.enable:=true
```

nodo gmm (no se podrá usar porque al ir moviendose la camara, el fondo cambia y por tanto, gmm no sirve):
```bash
ros2 run gmm_ros2 gmm_node
```
<br><br>




# Intel RealSense D435 en ROS 2

Configuración y explicación de la cámara Intel RealSense D435 usando `realsense2_camera` en ROS 2.

## 1. Introducción

La Intel RealSense D435 es una cámara RGB-D que combina:

- Cámara RGB (color).
- Dos cámaras infrarrojas (IR) para estimación de profundidad.
- Un proyector infrarrojo que ayuda al sistema estéreo en condiciones difíciles.

La cámara publica imágenes 2D y también puede generar nubes de puntos 3D.

En ROS 2 se utiliza el paquete:

```
realsense2_camera
```

---

# 2. Arquitectura de datos

La cámara funciona de esta manera:

```
                RealSense D435
                     |
       +-------------+-------------+
       |                           |
     RGB                         Depth
       |                           |
color/image_raw          depth/image_rect_raw
                                   |
                                   |
                         cálculo de profundidad
                                   |
                                   |
                    +--------------+--------------+
                    |                             |
              Imagen Depth                 PointCloud
                    |                             |
              DepthCloud RViz              PointCloud2 RViz
```

---

# 3. Lanzar la cámara

Ejemplo básico:

```bash
ros2 run realsense2_camera realsense2_camera_node
```

Con alineamiento de profundidad y generación de nube de puntos:

```bash
ros2 run realsense2_camera realsense2_camera_node \
  --ros-args \
  -p align_depth.enable:=true \
  -p pointcloud.enable:=true
```

---

# 4. Tópicos publicados

Comprobar:

```bash
ros2 topic list | grep camera
```

Ejemplo:

```
/camera/camera/color/image_raw

/camera/camera/depth/image_rect_raw

/camera/camera/aligned_depth_to_color/image_raw

/camera/camera/depth/color/points
```

---

# 5. Imagen RGB

La cámara RGB publica:

```
/camera/camera/color/image_raw
```

Tipo:

```
sensor_msgs/msg/Image
```

Se puede visualizar en RViz usando:

```
Add -> Image
```

---

# 6. Imagen de profundidad (Depth)

La cámara publica profundidad:

```
/camera/camera/depth/image_rect_raw
```

Tipo:

```
sensor_msgs/msg/Image
```

Cada píxel representa distancia.

Normalmente el formato es:

```
16UC1
```

donde el valor representa distancia en milímetros.

Ejemplo:

```
1000 = 1 metro
2000 = 2 metros
```

---

# 7. Depth alineado con RGB

Activando:

```
align_depth.enable:=true
```

se publica:

```
/camera/camera/aligned_depth_to_color/image_raw
```

Esto significa:

- Cada píxel de profundidad corresponde al mismo píxel de la imagen RGB.
- Es útil para detectar objetos en color y obtener su distancia.

Ejemplo:

```
RGB pixel:
    (320,240)

Depth pixel:
    (320,240)

Distancia:
    0.75 metros
```

---

# 8. PointCloud2

Activando:

```
pointcloud.enable:=true
```

la cámara genera directamente una nube 3D:

```
/camera/camera/depth/color/points
```

Tipo:

```
sensor_msgs/msg/PointCloud2
```

Cada punto contiene:

```
X
Y
Z
Color RGB
```

Ejemplo:

```
Punto 3D:

x = 0.12 m
y = -0.03 m
z = 0.75 m
```

---

# 9. Visualizar en RViz

## Opción recomendada: PointCloud2

En RViz:

```
Add
 |
 + PointCloud2
```

Seleccionar:

```
/camera/camera/depth/color/points
```

Configurar:

```
Fixed Frame:
camera_link
```

o un frame del robot conectado mediante TF.

---

# 10. ¿Qué es DepthCloud?

DepthCloud es un display antiguo de RViz.

No recibe una nube de puntos.

Recibe:

```
sensor_msgs/msg/Image
```

y calcula internamente:

```
Depth Image
      +
Camera Info
      |
      v
Puntos 3D
```

Necesita:

Imagen:

```
/camera/camera/aligned_depth_to_color/image_raw
```

Información de cámara:

```
/camera/camera/aligned_depth_to_color/camera_info
```

---

## Diferencia entre DepthCloud y PointCloud2

| | DepthCloud | PointCloud2 |
|-|-|-|
| Entrada | Imagen Depth | Nube 3D |
| Cálculo de puntos | RViz | Cámara |
| CPU usada | Mayor | Menor |
| Uso recomendado | Visualización rápida | Robótica |
| Tipo ROS | Image | PointCloud2 |

Para robots se recomienda:

```
PointCloud2
```

---

# 11. Infrarrojo estéreo de la RealSense D435

La D435 no obtiene profundidad midiendo directamente distancia.

Utiliza visión estéreo.

Tiene:

```
        IR izquierda          IR derecha

             \                 /
              \               /
               \             /

              Objeto

```

Las dos cámaras infrarrojas ven la misma escena desde posiciones diferentes.

La diferencia entre ambas imágenes se llama:

```
disparidad (disparity)
```

Con la disparidad se calcula la profundidad:

```
Más diferencia entre imágenes
        |
        v
Objeto más cerca


Menos diferencia
        |
        v
Objeto más lejos
```

---

# 12. ¿Para qué sirven las cámaras infrarrojas?

Las cámaras IR permiten:

## 1. Obtener profundidad

Son las responsables del cálculo 3D.

Sin ellas:

```
RGB solamente
=
imagen 2D
```

Con ellas:

```
RGB + IR estéreo
=
posición 3D
```

---

## 2. Funcionan con poca luz

La cámara RGB necesita iluminación.

Las cámaras IR pueden trabajar:

- En interiores.
- Con poca luz.
- Sin depender del color.

---

## 3. Evitan problemas con texturas pobres

Una pared blanca no tiene características visuales.

El sistema estéreo puede tener dificultades.

Por eso la D435 tiene un:

```
IR emitter
```

que proyecta un patrón infrarrojo.

Ese patrón crea textura artificial:

```
Pared lisa:

########


Con patrón IR:

# . ## . #
 . ## . #
# . ## .
```

Esto ayuda al cálculo de profundidad.

---

# 13. Activar/desactivar infrarrojos

Ver parámetros:

```bash
ros2 param list /camera/camera
```

Ejemplo:

Desactivar infrarrojos:

```bash
-p enable_infra1:=false
-p enable_infra2:=false
```

Mantener profundidad:

```bash
-p enable_depth:=true
```

---

# 14. Configuración recomendada para robótica

Para manipulación con robots:

```bash
ros2 run realsense2_camera realsense2_camera_node \
  --ros-args \
  -p enable_depth:=true \
  -p enable_color:=true \
  -p align_depth.enable:=true \
  -p pointcloud.enable:=true \
  -p depth_module.depth_profile:=848x480x30 \
  -p rgb_camera.color_profile:=640x480x30
```

Ventajas:

- 30 FPS.
- Buena precisión.
- Menor consumo CPU.
- Adecuado para ROS 2 y RViz.

---

# 15. Comprobaciones útiles

Ver tópicos:

```bash
ros2 topic list | grep camera
```

Ver tipo:

```bash
ros2 topic type /camera/camera/depth/color/points
```

Debe devolver:

```
sensor_msgs/msg/PointCloud2
```

Ver frecuencia:

```bash
ros2 topic hz /camera/camera/depth/color/points
```

Ver TF:

```bash
ros2 run tf2_tools view_frames
```

---

# 16. Resumen

Para robots:

Usar:

```
RealSense
    |
    |
/camera/camera/depth/color/points
    |
    |
RViz PointCloud2
```

No usar:

```
DepthCloud
```

salvo para pruebas rápidas.

La D435 calcula profundidad mediante:

```
Cámaras IR estéreo
        +
        |
        v
Disparidad
        |
        v
Profundidad
        |
        v
PointCloud 3D
```










































<!--
# Generar .urdf del .xacro de xArm6 de UFactory (pendiente de documentar con más detalle)
Dentro del contenedor de Docker de ROS2:
1. ```cd /home/isaac_sim/projects/ufactory_ros2/xarm_ros2```
2. ```colcon build --packages-select xarm_description```
3. ```source install/setup.bash```
4. ```cd /home/isaac_sim/projects/ufactory_ros2/xarm_ros2/xarm_description/urdf```
5. ```xacro xarm_device.urdf.xacro   dof:=6   robot_type:=xarm   hw_ns:=xarm   limited:=true   velocity_control:=false   effort_control:=false   add_gripper:=false   -o xarm6.urdf```
6. ```xacro xarm_device.urdf.xacro   dof:=6   robot_type:=xarm   hw_ns:=xarm   limited:=true   velocity_control:=false   effort_control:=false   add_gripper:=true   -o xarm6_with_gripper.urdf```
7. ```xacro xarm_device.urdf.xacro robot_type:=uf850 dof:=6 hw_ns:=xarm limited:=true velocity_control:=false effort_control:=false add_gripper:=false -o uf850.urdf```
8. ```xacro xarm_device.urdf.xacro robot_type:=uf850 dof:=6 hw_ns:=xarm limited:=true velocity_control:=false effort_control:=false add_gripper:=true -o uf850_with_gripper.urdf```


# Para ejecutar entrenamiento UFXarm6:
Copiar la carpeta ``/workspace/isaaclab/_isaac_sim/projects/ufactory_ros2/isaac-sim/scripts/train/base/uf_xarm6`` en ``/workspace/isaaclab/source/isaaclab_tasks/isaaclab_tasks/manager_based/manipulation/reach/config``.

Ejecutar ``./isaaclab.sh -p scripts/reinforcement_learning/skrl/train.py --task Isaac-Reach-XArm6-v0 --num_envs 600``, para ver los logs ``./isaaclab.sh -p -m tensorboard.main --logdir logs/skrl/reach_franka/``, para play ``./isaaclab.sh -p scripts/reinforcement_learning/skrl/play.py --task Isaac-Reach-XArm6-v0 --num_envs 32``

# Para controlar el robot real desde MoveIt
``ros2 launch xarm_moveit_config xarm6_moveit_realmove.launch.py robot_ip:=192.168.1.238 auto_enable:=true``

Para lanzar el controller sin moveit2: ``ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.238``

```
cd ~/dev_ws/
# launch xarm_driver_node:
ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.117

# enable all joints:
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetInt16ById "{id: 8, data: 1}"

# disable
ros2 service call /xarm/motion_enable xarm_msgs/srv/SetInt16ById "{id: 8, data: 0}"

# set proper mode (0) and state (0)
ros2 service call /xarm/set_mode xarm_msgs/srv/SetInt16 "{data: 0}"
ros2 service call /xarm/set_state xarm_msgs/srv/SetInt16 "{data: 0}"

# Cartesian linear motion: (unit: mm, rad)
ros2 service call /xarm/set_position xarm_msgs/srv/MoveCartesian "{pose: [300, 0, 250, 3.14, 0, 0], speed: 50, acc: 500, mvtime: 0}"   

# joint motion for xArm6: (unit: rad)
ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [-0.58, 0, 0, 0, 0, 0], speed: 0.35, acc: 10, mvtime: 0}"
```

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.5, 0.0, 0.0, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, -0.7, -0.95, 0.0, 0.0, 0.0], speed: 0.5, acc: 0.5, wait: true}"``

Detecta colisión con si mismo: ``ros2 service call /xarm/set_servo_angle xarm_msgs/srv/MoveJoint "{angles: [0.0, 0.2, 0.1, 0.0, 0.0, 0.0], speed: 0.1, acc: 0.1, wait: true}"``

Códigos de error: https://github.com/xArm-Developer/xArm-Python-SDK/blob/master/doc/api/xarm_api_code.md

ros2 topic echo /xarm/robot_states

ros2 service type /xarm/motion_enable

# Para controlar el motor lineal desde ROS2

Hay que activar los servicios del motor lineal. Eso se hace en ``xarm_ros2/xarm_api/config/xarm_params.yaml`` o en la versión compilada en ``/home/xarm_ws/install/xarm_api/share/xarm_api/config/xarm_params.yaml``

```yaml
set_linear_motor_stop: false
clean_linear_motor_error: false
get_linear_motor_pos: true
get_linear_motor_status: true
get_linear_motor_error: true
get_linear_motor_is_enabled: true
get_linear_motor_on_zero: true
get_linear_motor_sci: true 
get_err_warn_code: false
get_linear_motor_sco: true    
set_linear_motor_enable: true 
set_linear_motor_speed: true
set_linear_motor_back_origin: true 
set_linear_motor_pos: true         
```


```bash
ros2 launch xarm_api xarm6_driver.launch.py robot_ip:=192.168.1.211
```

```bash
?? ros2 service call /xarm/set_linear_motor_enable xarm_msgs/srv/SetInt16 "{data: 1}" ??
```

```bash
ros2 service call /xarm/get_linear_motor_is_enabled xarm_msgs/srv/GetInt16 "{}"
```

```bash
ros2 service call /xarm/set_linear_motor_pos xarm_msgs/srv/LinearMotorSetPos "{pos: 650, speed: 150, wait: true, timeout: 100.0, auto_enable: true}"
```

-->