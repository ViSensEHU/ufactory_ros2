# settings.py

WIN_NAME   = 'RealSense-D435'
CAM_WIDTH  = 640
CAM_HEIGHT = 480

# use open-loop solution when robot height is over OPEN_LOOP_HEIGHT
OPEN_LOOP_HEIGHT = 340   # mm
GGCNN_IN_THREAD  = False

# show the grasp image of ggcnn or not, otherwise show native depth images.
SHOW_GRASP_IMG   = True

# rgb camera calibration result
EULER_EEF_TO_COLOR_OPT   = [0.067052239, -0.0311387575, 0.021611456, -0.004202176, -0.00848499, 1.5898775]
EULER_COLOR_TO_DEPTH_OPT = [0.015, 0, 0, 0, 0, 0]

# The range of motion of the robot grasping
# If it exceeds the range, it will return to the initial detection position.
GRASPING_RANGE = [-180, 650, -480, 480] # [x_min, x_max, y_min, y_max]

# initial detection position
DETECT_XYZ     = [220.5, 0, 575] # [x, y, z]

# release grasping pos
RELEASE_XYZ    = [0, 360.5, 488] # [x, y, z]

# lift offset based on DETECT_XYZ[2] after grasping or release
LIFT_OFFSET_Z  = 0 # lift_height = DETECT_XYZ[2] + LIFT_OFFSET_Z

# The distance between the gripping point of the robot grasping and the end of the robot arm flange
# The value needs to be fine-tuned according to the actual situation.
GRIPPER_Z_MM   = 150

# minimum z for grasping
GRASPING_MIN_Z = 0
