El fichero ``xArm6_sensorFuerza_motorLineal.usd`` contiene el asset con:
- robot UFactory xArm6 (importado de NVIDIA Robots Assets)
- sensor de fuerza, 
- stand de la cámara, 
- cámara 
- motor lineal.


Además, incluye los siguientes OmniGraphs:
- ``ft_sensor``: este grafo publica en el tópico de ROS2 ``ft_sensor`` las medidas del sensor de fuerza. 
Utiliza el mensaje estándar de ROS2 ``WrenchStamped`` del paquete ``geometry_msgs`` y subcarpeta ``msg``, utilizado para sensores de fuerza de 6 ejes (F/T sensor). 
Las lecturas del sensor se obtienen con el script ``ft_sensor.py`` integrado en el grafo. Para más información, ver el ``README.md`` de la carpeta ``ft_sensor``.

- ``camara/Realsense_D435/Publishers``: publicadores de la imagen RGB en el tópico de ROS2 ``/rgb`` y sensor de profundidad en ``/depth``.
Ambos usan el tipo de mensaje de ROS2 ``sensor_msgs/msg/Image``.

- ``ROS_JointStates``: publica en el tópico de ROS2 ``/joint_states`` las posiciones de cada articulación del robot y recibe por el tópico ``/joint_command`` las posiciones objetivo de cada articulación en ***radianes**.
Ambos usan el mensaje de tipo ``sensor_msgs/msg/JointState``. 

    A modo de prueba, se puede mandar por terminal una posición objetivo de la siguiente manera (donde ``Component2_to_Baselink`` es la joint del motor lineal y ``drive_joint`` la pinza): 
    ```bash
    ros2 topic pub /joint_command sensor_msgs/JointState "
    name:
    - 'Component2_to_BaseLink'
    - 'joint1'
    - 'joint2'
    - 'joint3'
    - 'joint4'
    - 'joint5'
    - 'joint6'
    - 'drive_joint'
    position: [-0.335, -0.87, -1.40, -0.35, 1.5708, 1.4, 1.5708, 0.84]
    " -1
    ```