El sensor de fuerza está integrado en el .usd (``805conCamara.usd``) en el Action Graph ``ft_sensor``.

Este grafo utiliza el mensaje estándar de ROS2 ``WrenchStamped`` del paquete ``geometry_msgs`` y subcarpeta ``msg``, utilizado para sensores de fuerza de 6 ejes (F/T sensor). El mensaje se publica al tópico ``ft_sensor``.

Las imágenes en ``img/old/`` son capturas de pantalla del grafo anterior, pero el ArticulationState en OmniGraph únicamente lee de Joints con DOF, es decir, no lee FixedJoints y por tanto, no nos servía. Las imágenes en ``img/`` son las capturas actuales

Consecuentemente, se ha integrado un script de Python en el OmniGraph, ``ft_sensor.py``, que obtiene los valores de fuerza, y los saca como output para mandar el bloque de ROS2 Publisher.

El fichero ``sensor_fuerza.py`` es un fichero Python de respaldo para ejecutar en ``Window > Script Editor``.

Referencias:
[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_physics_articulation_force.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/sensors/isaacsim_sensors_physics_articulation_force.html)

[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.api/docs/index.html#isaacsim.core.api.robots.Robot.get_measured_joint_forces](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.api/docs/index.html#isaacsim.core.api.robots.Robot.get_measured_joint_forces)

[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.nodes/docs/ogn/OgnIsaacArticulationState.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/py/source/extensions/isaacsim.core.nodes/docs/ogn/OgnIsaacArticulationState.html)

[Definición Mensaje ROS2 WrenchStamped](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/WrenchStamped.html)

[Definición Mensaje ROS2 Wrench](https://docs.ros.org/en/jazzy/p/geometry_msgs/msg/Wrench.html)

[https://docs.omniverse.nvidia.com/extensions/latest/ext_omnigraph/node-library/nodes/omni-graph-scriptnode/scriptnode-1.html](https://docs.omniverse.nvidia.com/extensions/latest/ext_omnigraph/node-library/nodes/omni-graph-scriptnode/scriptnode-1.html)

[https://docs.omniverse.nvidia.com/kit/docs/omni.graph.scriptnode/latest/GeneratedNodeDocumentation/OgnScriptNode.html](https://docs.omniverse.nvidia.com/kit/docs/omni.graph.scriptnode/latest/GeneratedNodeDocumentation/OgnScriptNode.html)

[https://docs.isaacsim.omniverse.nvidia.com/5.1.0/omnigraph/omnigraph_scripting.html](https://docs.isaacsim.omniverse.nvidia.com/5.1.0/omnigraph/omnigraph_scripting.html)