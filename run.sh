xhost +local:docker
docker run -e DISPLAY=$DISPLAY \
           -e USER=$USER \
           -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
           -v ./xarm_ros2:/home/$USER/xarm_ros2/ \
           -it \
           --rm \
            xarm_ros2:jazzy

# --network host \
# -v /dev/shm:/dev/shm \

