docker run -it --rm \
    --privileged \
    --net=host \
    --device /dev/dri:/dev/dri \
    --device /dev/bus/usb \
    -v "$(pwd)":/home/xarm6/Documents/ufactory_ros2:rw \
    --name ros2_jazzy_realsense_vision \
    ros2-arm64-jazzy-vision:latest
