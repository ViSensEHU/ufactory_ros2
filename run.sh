#en el host es necesario: sudo prime-select nvidia
# y al ejecutar "glxinfo | grep "OpenGL renderer" que aparezca NVIDIA
#xhost +local:docker
#docker run -it --rm \
#    --gpus all \
#    --runtime=nvidia \
#    --network=host \
#    -e USER=$USER \
#    -e DISPLAY=$DISPLAY \
#    -e NVIDIA_VISIBLE_DEVICES=all \
#    -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute \
#    -e RMW_IMPLEMENTATION=rmw_fastrtps_cpp \
#    -v /tmp/.X11-unix:/tmp/.X11-unix \
#    -v ./xarm_ros2:/home/$USER/xarm_ros2 \
#    -v ./control_ws:/home/$USER/control_ws \
#    --name xarm_ros2 \
#    visensehu/xarm_jazzy:v1

xhost +local:docker
docker run -e DISPLAY=$DISPLAY \
           -e USER=$USER \
           -e NVIDIA_VISIBLE_DEVICES=all \
           -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute \
           --runtime=nvidia \
           -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
           --device /dev/dri:/dev/dri \
           -it \
           --rm \
           --network=host \
           --gpus all \
           --name xarm_ros2 \
           -v ./xarm_ros2:/home/$USER/xarm_ros2 \
           -v ./control_ws:/home/$USER/control_ws \
           arambarricalvoj/xarm_ros2:jazzy_isaacsim

# --network host \
# -v /dev/shm:/dev/shm \

# --device /dev/dri:/dev/dri \
# --gpus all \ con NVIDIA no funciona, debe estar algo mal configurado

#xhost +local:*
#docker run -e DISPLAY=$DISPLAY \
#           -e USER=$USER \
#           -v /tmp/.X11-unix/:/tmp/.X11-unix/ \
#           -v ./eduros2_lego:/home/$USER/eduros2_lego/ \
#           -v /dev/input:/dev/input \
#           --device-cgroup-rule='c 13:* rmw' \
#           -p 5000:5000/udp \
#           -p 5001:5001/udp \
#           -p 5002:5002/udp \
#           -p 5003:5003/udp \
#           -p 5004:5004/udp \
#           --device /dev/dri:/dev/dri \
#           --device /dev/input:/dev/input \
#           -it \
#           --rm \
#           --gpus all \
#           --name eduros2_control_inteligente \
#           arambarricalvoj/eduros2_ev3:control_inteligente
