xhost +local:docker
sudo docker run -it --rm \
    --gpus all \
    --runtime=nvidia \
    --net=host \
    -e USER=$USER \
    -e DISPLAY=$DISPLAY \
    -e NVIDIA_VISIBLE_DEVICES=all \
    -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute \
    -v /tmp/.X11-unix:/tmp/.X11-unix \
    -v "$(pwd)":/home/isaac_sim/Documents/ufactory_ros2:rw \
    --device /dev/dri:/dev/dri \
    --name xarm_ros2 \
    xarm:jazzy-yolo-gpu
    #visensehu/xarm_ros2:jazzy

# -v ./xarm_ros2:/home/$USER/xarm_ros2 \
