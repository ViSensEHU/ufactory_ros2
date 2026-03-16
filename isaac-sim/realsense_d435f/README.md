Esta carpeta contiene los ficheros correspondientes a la cámara RealSense D435F.

Esta cámara no está incorporada en Isaac Sim, por lo que se ha tenido que crear. Para ello, en un primer momento se creó un prisma con las dimensiones de la cámara, fichero CAD ``3d/prisma_rs_d435d.stl``, pero después se encontró un diseño completo de la misma en la siguiente plataforma: [grabcad.com/library/intel-realsense-d435-camera-1](grabcad.com/library/intel-realsense-d435-camera-1). 

El diseño descargado corresponde a los ficheros ``3d/rs_d435d.stl``, ``3d/rs_d435d.stp`` y ``intel-realsense-d435-camera-1.snapshot.3.zip``. Isaac Sim daba problemas al cargar el archivo STEP, por lo que se ha usado el STL.

El fichero ``usd/rs_d435f.usd`` he el asset de la cámara en Isaac Sim, que incorpora colisiones, Rigid Body, los parámetros intrínsecos de la cámara configurados y el OmniGraph ``Publishers``.

Dicho grafo publica la imagen RGB en el tópico de ROS2 ``/rgb`` y el sensor de profundidad en ``/depth``. Ambos usan el tipo de mensaje de ROS2 ``sensor_msgs/msg/Image``.

Los parámetros de la cámara de obtienen del datasheet en el fichero ``RealSense-D400-Series-Datasheet-Dec-2025.pdf`` o en el enlace [https://www.intel.la/content/www/xl/es/architecture-and-technology/realsense-overview.html](https://www.intel.la/content/www/xl/es/architecture-and-technology/realsense-overview.html).

Para la configuración de la cámara en Isaac Sim se ha seguido la siguiente documentación:
- [https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_camera.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_camera.html)
- [https://docs.isaacsim.omniverse.nvidia.com/5.1.0/assets/usd_assets_camera_depth_sensors.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/assets/usd_assets_camera_depth_sensors.html)

En cualquier caso, para comprobar cómo se ha configurado tanto la cámara como el sensor de profundidad, se puede explorar el ``usd/rs_d435f.usd`` en Isaac Sim.