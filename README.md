
# NOTA: la carpeta ``ri-misc`` contiene el proyecto que estoy desarrollando en la asignatura de Robótica Industrial del Máster. El fichero ``ri-misc/memoria/main.pdf`` es la memoria en desarrollo en la que describo el robot de UFactory, por lo que es de interés para conocer el brazo manipulador. En este sentido, en dicha carpeta se encuentran varios manuales y trabajos publicados en internet en los que han utilizado en mismo robot.

# NOTA2: la cámara en gazebo harmonic funciona diferente a classic. Ya no funciona el plugin, y no he encontrado documentación de cómo hacerlo, solo este repo: https://github.com/MOGI-ROS/Week-5-6-Gazebo-sensors que he conseguido ejecutar en un docker para aprender a usar la cámara. Todavía No he documentado ni compartido el dockerfile para ejecutarlo, lo tengo yo en local porque he conseguido ejecutarlo (con errores pero la cámara va y es lo que nos interesa) y ahora tendría que descubrir cómo lo hace y aprender, y ya con eso documentar.
--

# UFactory XArm6 ROS2 + Docker - EIB/EHU
In order to build the image, you can either follow the steps manually or run the bash script ``build.sh``, but first make sure to meet all the prerrequisites!<br>
In order to run the container, you can run it manually as shown below or run the bash script ``run.sh``.

Click here to move automatically to [Interacting with UFactory XArm6 ](#interacting-with-ufactory-xarm6)
<br><br>

# Specifications
This repository has been run with the following host specifications:

OS: ``Ubuntu 24.04.X LTS``<br>
RAM: ``32 GB``<br>
Processor: ``13th Gen Intel® Core™ i7-13650HX × 20``<br>
Graphics card: ``NVIDIA GeForce RTX 4060 Laptop GPU``<br>
Graphics card memory: ``8 GB``<br>
Needed disk space: ``6 GB``<br>
NVIDIA GPU drivers version: ``535.129.03`` or later<br>

*It should work in previous releases as 20.04 and 22.04.

### ROS2 version
``ROS2 Jazzy Desktop``

### Docker version (at least, it should work with this version or later onea)
``Client: Docker Engine - Community``<br>
``Version:           27.3.1``<br>
``API version:       1.47``<br>
``Go version:        go1.22.7``<br>
``Git commit:        ce12230``<br>
``Built:             Fri Sep 20 11:40:59 2024``<br>
``OS/Arch:           linux/amd64``<br>
``Context:           default``<br>

``Server: Docker Engine - Community``<br>
`Engine:`<br>
` Version:          27.3.1`<br>
` API version:      1.47 (minimum version 1.24)`<br>
`Go version:       go1.22.7`<br>
`Git commit:       41ca978`<br>
`Built:            Fri Sep 20 11:40:59 2024`<br>
`  OS/Arch:          linux/amd64`<br>
`  Experimental:     false`<br>
` containerd:`<br>
`  Version:          1.7.22`<br>
`  GitCommit:        7f7fdf5fed64eb6a7caf99b3e12efcf9d60e311c`<br>
` runc:`<br>
`  Version:          1.1.14`<br>
 ` GitCommit:        v1.1.14-0-g2c9f560`<br>
 `docker-init:`<br>
  `Version:          0.19.0`<br>
 ` GitCommit:        de40ad0`<br>
<br><br>

# Prerequisites
Gazebo UFacotry simulations with integrated processor's GPU works very slowly, so it is strongly recommended to run them with a dedicated GPU (in this case, NVIDIA). For this reason, it is necessary to install the NVIDIA drivers, as well as the NVIDIA Container Toolkit, in order to use the NVIDIA GPU within Docker.

- NVIDIA Drivers installation: https://ubuntu.com/server/docs/nvidia-drivers-installation<br>
Once GPU drivers are installed, check it with:
```bash
nvidia-smi
```

- Docker installation and executing without sudo:
```bash
curl -fsSL https://get.docker.com -o get-docker.sh
sudo sh get-docker.sh
```
```bash
# Post-install steps for Docker
sudo groupadd docker # Create group
sudo usermod -aG docker $USER # Add current user to docker group
newgrp docker # Log in docker group
```
```bash
#Verify Docker installation
docker run hello-world
```

- NVIDIA Container Toolkit installation:
```bash
# Configure the repository
curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg \
  && curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
    sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
    sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list \
  && \
    sudo apt-get update

# Install the NVIDIA Container Toolkit packages
sudo apt-get install -y nvidia-container-toolkit
sudo systemctl restart docker

# Configure the container runtime
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# Verify NVIDIA Container Toolkit
docker run --rm --runtime=nvidia --gpus all ubuntu nvidia-smi
```

- Generate NGC API Key: https://docs.nvidia.com/ngc/ngc-overview/index.html#generating-api-key
- Log in to NGC:
```bash
docker login nvcr.io
```
```bash
Username: $oauthtoken
Password: <Your NGC API Key>
WARNING! Your password will be stored unencrypted in /home/username/.docker/config.json.
Configure a credential helper to remove this warning. See
credentials-store
Login Succeeded
```

- Activate NVIDIA GPU X Server (host running GUI with NVIDIA GPU instead of Intel/AMD one):
```bash
sudo prime-select nvidia
sudo reboot
```
This step is needed as Docker inherits X Server (GUI) from the host, any of the following will fail in order to run NIS with NVIDIA GPU in Docker:
```bash
sudo prime-select intel
sudo prime-select on-demand
```
Next, for the changes to take effect, restart the host:
```bash
sudo reboot
```
Check the host is running with NVIDIA GPU:
```bash
sudo apt install mesa-utils
glxinfo | grep "OpenGL renderer"
```

You must see an output similar to: ```OpenGL renderer string: NVIDIA GeForce RTX 4060 Laptop GPU/PCIe/SSE2```. If you don't see ``NVIDIA``, then you are not running wiht NVIDIA GPU. You must also run this command inside the Docker container to verify that Docker is using the GPU. If it is not, please report an issue.
<br><br>


# Build Docker image
```bash
docker build -t {IMAGE_NAME}:{TAG} .
```
Example:
```bash
docker build -t xarm_ros2:jazzy .
```

# Run container
Allow running graphic interfaces in the container:
```bash
xhost +local:docker
```
Run the container with the needed configuration:
```bash
xhost +local:docker
docker run -it --rm \
       --gpus all \
       --runtime=nvidia \
       -e DISPLAY=$DISPLAY \
       -e NVIDIA_VISIBLE_DEVICES=all \
       -e NVIDIA_DRIVER_CAPABILITIES=graphics,utility,compute \
       -v /tmp/.X11-unix:/tmp/.X11-unix \
       -v ./xarm_ros2:/home/$USER/xarm_ros2 \
       --name xarm_ros2 \
       xarm_ros2:jazzy
```
The volume ```-v ./xarm_ros2:/home/$USER/xarm_ros2``` is intended to be the working directory.

REMEMBER: if you want to share a folder between the host and the container, mount it adding the next flag to the previous command:
```bash
-v HOST_PATH:PATH_IN_CONTAINER
```
```bash
-v ~/Documents/isaac_sim/PROJECT_ID:~/PROJECT_ID
```
<br><br>

# Build and run with bash scripts 
When you meet the prerequisites, you can automatically build the image using the ```build.sh``` script and run the container using the ```run.sh``` script.

Add execution permissions:
```bash
chmod u+x build.sh run.sh
```

Build the image:
```bash
./build.sh
```

Once the image has been built, whenever you want to run the container, just execute the following:
```bash
./run.sh
```
<br><br>


# Interacting with UFactory XArm6 
1. Start the Docker container:
    ```bash
    ./run.sh
    ```

2. Inside the container, check that Docker is running with dedicated GPU (NVIDIA):
    ```bash
    sudo apt install mesa-utils
    glxinfo | grep "OpenGL renderer"
    ```
    You must see an output similar to: ```OpenGL renderer string: NVIDIA GeForce RTX 4060 Laptop GPU/PCIe/SSE2```. If you don't see ``NVIDIA``, then you are not running wiht NVIDIA GPU. In that case, please report an issue.

3. Open new terminals in the Docker container (as many as you need). In a host's terminal run:
    ```bash
    docker exec -it xarm_ros2 bash
    ```
    ``xarm_ros2`` stand for the name given to the container in the ``run.sh`` script.
    
    Great! You are inside the running Docker container!

TIP: to manage several terminals in the same screen I use [Tilix](https://gnunn1.github.io/tilix-web/) instead of Terminator (Termux). You can install it easily:
```bash
sudo apt update && sudo apt install tilix -y
```
<br><br>


## (to be documented... ;) ) lo siguiente va todo dentro del contenedor de Docker, si se ejecuta en local no funciona!
## Visualizar en RVIZ2 y mover las joints
En una terminal: 
```bash
ros2 launch xarm_description xarm6_rviz_display.launch.py add_gripper:=true
```

En otra terminal:
```bash
ros2 run joint_state_publisher_gui joint_state_publisher_gui
```
<br><br>

## xArm moveit config
ros2 launch xarm_moveit_config xarm6_moveit_fake.launch.py [add_gripper:=true]
<br><br>

## xArm planner
En una terminal:
```bash
ros2 launch xarm_planner xarm6_planner_fake.launch.py [add_gripper:=true]
```

En otra terminal:
```bash
ros2 launch xarm_planner test_xarm_planner_api_joint.launch.py dof:=6 robot_type:=xarm
```
o 
```bash
ros2 launch xarm_planner test_xarm_planner_api_pose.launch.py dof:=6 robot_type:=xarm
```
<br><br>