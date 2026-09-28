xhost +local:docker
sudo docker run -it --rm \
    -e USER=$USER \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v ./ws:/home/$USER/ws \
    --device /dev/dri:/dev/dri \
    --name xarm_ros2 \
    visensehu/xarm_ros2:jazzy

# -v ./xarm_ros2:/home/$USER/xarm_ros2 \
