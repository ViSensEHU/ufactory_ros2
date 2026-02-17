El sensor de fuerza está integrado en el .usd (``805conCamara.usd``) en el Action Graph ``tf_sensor``.

Este grafo utiliza el mensaje estándar de ROS2 ``WrenchStamped`` del paquete ``geometry_msgs`` y subcarpeta ``msg``, utilizado para sensores de fuerza de 6 ejes (F/T sensor). El mensaje se publica al tópico ``ft_sensor``.

Las imágenes en esta ruta son capturas de pantalla de dicho grafo, y el fichero ``sensor_fuerza.py`` cómo leer el sensor de fuerza desde Python.

Referencias:
[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_physics_articulation_force.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_physics_articulation_force.html)

[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.api/docs/index.html#isaacsim.core.api.robots.Robot.get_measured_joint_forces](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.api/docs/index.html#isaacsim.core.api.robots.Robot.get_measured_joint_forces)

[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.nodes/docs/ogn/OgnIsaacArticulationState.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.nodes/docs/ogn/OgnIsaacArticulationState.html)

[Definición Mensaje ROS2 WrenchStamped](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/WrenchStamped.html)

[Definición Mensaje ROS2 Wrench](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Wrench.html)