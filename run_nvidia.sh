#en el host es necesario: sudo prime-select nvidia
# y al ejecutar "glxinfo | grep "OpenGL renderer" que aparezca NVIDIA
xhost +local:docker
docker run -it --rm \
    --gpus all \
    --runtime=nvidia \
    -e USER=$USER \
    -e DISPLAY=$DISPLAY \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ./xarm_ros2:/home/$USER/xarm_ros2 \
    -v ./control_ws:/home/$USER/control_ws \
    --name xarm_ros2 \
    arambarricalvoj/xarm_ros2:jazzy
