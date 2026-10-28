xhost +local:docker
sudo docker run -it --rm \
    --net=host \
    -e USER=$USER \
    -e DISPLAY=$DISPLAY \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)":/home/javierarambarricalvo/Documents/ufactory_ros2:rw \
    --device /dev/dri:/dev/dri \
    --name xarm_ros2 \
    visensehu/xarm_ros2:jazzy

# -v ./xarm_ros2:/home/$USER/xarm_ros2 \
