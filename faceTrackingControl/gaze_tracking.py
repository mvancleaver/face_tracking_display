
############################################################################################################
###################################################### - Setup 
############################################################################################################

import cv2
import time
import board
import busio
import json
import numpy as np

######### IMU Driver Init 
import adafruit_bno055 as imu
i2c = busio.I2C(board.SCL, board.SDA) 
feedback = imu.BNO055_I2C(i2c)

######### PWM Board Init
from adafruit_servokit import ServoKit
i2c_1 = busio.I2C(board.SCL_1, board.SDA_1)  
axis = ServoKit(channels=16, i2c=i2c_1)

######### Realsense Depth Camera 
import pyrealsense2 as rs
# Create a pipeline
pipeline = rs.pipeline() 
#Create a config and configure the pipeline to stream
#  different resolutions of color and depth streams
config = rs.config()
config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)
# Start streaming
profile = pipeline.start(config)
# Getting the depth sensor's depth scale (see rs-align example for explanation)
depth_sensor = profile.get_device().first_depth_sensor()
depth_scale = depth_sensor.get_depth_scale()
print("Depth Scale is: " , depth_scale)
# We will be removing the background of objects more than
#  clipping_distance_in_meters meters away
clipping_distance_in_meters = 1 #1 meter
clipping_distance = clipping_distance_in_meters / depth_scale
# Create an align object
# rs.align allows us to perform alignment of depth frames to others frames
# The "align_to" is the stream type to which we plan to align depth frames.
align_to = rs.stream.color
align = rs.align(align_to)

######### Gaze Init 
from gaze_tracking import GazeTracking
gaze = GazeTracking()
webcam = cv2.VideoCapture(0)

############################################################################################################
###################################################### - Motion Primatives + Controller 
############################################################################################################

######### Axis Motion Primatives
x_axis_control = axis.servo[0].angle
x_home = feedback.euler[0]
x_feedback = feedback.euler[0]
x_setpoint = x_home

def home_X():
    print("Homing X")

def move_X():
    print("Moving X")


y_axis_control = axis.servo[1].angle
y_home = feedback.euler[1]
y_feedback = feedback.euler[1]
y_setpoint = y_home

def home_Y():
    print("Homing Y")

def move_Y():
    print("Moving Y")


z_axis_control = axis.servo[2].angle
z_home = feedback.euler[2]
z_feedback = feedback.euler[2]
z_setpoint = z_home

def move_Z():
    print("Moving Z")

def home_Z():
    print("Homing Z")


def home_All():
    home_X()
    home_Y()
    home_Z()


############################################################################################################
###################################################### - System Main 
############################################################################################################

try:
    while True:
        # Get frameset of color and depth
        frames = pipeline.wait_for_frames()
        # frames.get_depth_frame() is a 640x360 depth image

        # Align the depth frame to color frame
        aligned_frames = align.process(frames)

        # Get aligned frames
        aligned_depth_frame = aligned_frames.get_depth_frame() # aligned_depth_frame is a 640x480 depth image
        color_frame = aligned_frames.get_color_frame()

        # Validate that both frames are valid
        if not aligned_depth_frame or not color_frame:
            continue

        depth_image = np.asanyarray(aligned_depth_frame.get_data())
        color_image = np.asanyarray(color_frame.get_data())

        # Remove background - Set pixels further than clipping_distance to grey
        grey_color = 153
        depth_image_3d = np.dstack((depth_image,depth_image,depth_image)) #depth image is 1 channel, color is 3 channels
        bg_removed = np.where((depth_image_3d > clipping_distance) | (depth_image_3d <= 0), grey_color, color_image)
   
        # Grab a color frame and process Gaze info 
        gaze.refresh(color_image)
        new_frame = gaze.annotated_frame()
        text = ""
        if gaze.is_right():
            text = "Looking right"
            move_X()
        elif gaze.is_left():
            text = "Looking left"
            move_X()
        elif gaze.is_center():
            text = "Looking center"
            home_ALL()

        cv2.putText(new_frame, text, (60, 60), cv2.FONT_HERSHEY_DUPLEX, 2, (255, 0, 0), 2)
        cv2.imshow("Demo", new_frame)
        if cv2.waitKey(1) == 27:
            break

         # Render images
        #depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.03), cv2.COLORMAP_JET)
        #images = np.hstack((bg_removed, depth_colormap))
        #cv2.namedWindow('Align Example', cv2.WINDOW_AUTOSIZE)
        #cv2.imshow('Align Example', images)
        #key = cv2.waitKey(1)
        # Press esc or 'q' to close the image window
        #if key & 0xFF == ord('q') or key == 27:
        #    cv2.destroyAllWindows()
        #    break
        # Print IMU Data to JSON
        #print("Euler angle X: {}".format(feedback.euler[0]))
        #print("Euler angle Y: {}".format(feedback.euler[1]))
        #print("Euler angle Z: {}".format(feedback.euler[2]))

        data = {"eurler":{"X":feedback.euler[0],"Y":feedback.euler[1],"Z":feedback.euler[2]}}
        with open("data_file.json", "w") as write_file:
            json.dump(data, write_file)
finally:
    pipeline.stop()