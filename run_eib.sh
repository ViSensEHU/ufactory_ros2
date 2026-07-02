xhost +local:docker
sudo docker run -it --rm \
    --privileged \
    -e USER=$USER \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ./xarm_ros2:/home/$USER/xarm_ros2 \
    -v ./martin_ws:/home/$USER/martin_ws \
    --device /dev/dri:/dev/dri \
    --device /dev/bus/usb \
    --name xarm_ros2 \
    xarm_ros2:jazzy-vision
