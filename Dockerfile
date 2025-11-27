FROM osrf/ros:jazzy-desktop-full

ENV DEBIAN_FRONTEND=noninteractive

# Utilidades básicas
RUN apt-get update && apt-get install -y \
    git \
    python3-pip \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

# Instalar MoveIt 2 (no viene en desktop-full)
RUN apt-get update && apt-get install -y \
    ros-jazzy-moveit \
    && rm -rf /var/lib/apt/lists/*

# Crear workspace
WORKDIR /home/xarm_ws/src

# Clonar el repo xarm_ros2 (rama jazzy)
RUN git clone https://github.com/xArm-Developer/xarm_ros2.git --recursive -b jazzy

WORKDIR /home/xarm_ws

# Instalar dependencias vía rosdep
RUN apt-get update && \
    rosdep update && \
    rosdep install --from-paths src --ignore-src -r -y --rosdistro jazzy

# Compilar con colcon
RUN . /opt/ros/jazzy/setup.sh && \
    colcon build --symlink-install

# Configurar entorno por defecto
RUN echo "source /opt/ros/jazzy/setup.bash" >> ~/.bashrc && \
    echo "source /home/xarm_ws/install/setup.bash" >> ~/.bashrc

WORKDIR /home/xarm_ws
