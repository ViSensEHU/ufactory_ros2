# Trabajo final sobre la materia
Esta rama corresponde al proyecto final de la asignatura de Robótica Industrial del Máster en Ingeniería de Sistemas y Control de la Universidad Complutense de Madrid y la UNED, curso académico 2025/2026.

En ``memoria.pdf`` se encuentra la memoria descriptiva del proyecto con todo el código.

El directorio ``matlab/`` contiene los ficheros ``.m`` para ejecutar el controlador completo explicado en la memoria.

El directorio ``control_ws`` contiene el nodo de ROS2 en C++ expuesto en la memoria con el que se controla el brazo robótico *UFactory xArm6*.

En este README se explica cómo ejecutar el nodo de ROS2.

## Descargar o construir la imagen Docker
Si quieres construir la imagen, ejecuta el script ``build.sh``
```bash
sudo chmod u+x build
./build.sh
```

Si prefieres descargar la imagen:
```bash
docker pull arambarricalvoj/xarm_ros2:jazzy
```

# Ejecutar la imagen Docker
En una terminal ejecutar:
```bash
sudo chmod u+x run.sh
./run.sh
```

Si se tiene configurado el NVIDIA Container Toolkit y la GPU en el host, se puede ejecutar con ``run_nvidia.sh``. Las instrucciones se encuentran en la rama principal.

En otra terminal acceder al contenedor activo:
```bash
docker exec -it xarm_ros2 bash
```

# Ejecutar proyecto
En una terminal ejecutar:
```bash
ros2 launch xarm_moveit_config xarm6_moveit_gazebo.launch.py
```

En la otra terminal ejecutar:
```bash
cd /home/$USER/control_ws
colcon build
source install/setup.bash
ros2 run xarm6_cpp_control xarm6_action_client
```