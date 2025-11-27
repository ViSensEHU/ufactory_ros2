xhost +local:docker
docker run -e DISPLAY=$DISPLAY \
           -e USER=$USER \
           -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
           -v ./xarm_ros2:/home/$USER/xarm_ros2/ \
           -it \
           --rm \
            osrf/ros:jazzy-desktop-full

# --network host \
# -v /dev/shm:/dev/shm \

