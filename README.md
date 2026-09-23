# Autonomous-Aerial-Drone-Tracking-using-Vision-feedback

# 🚁 Aerial Object Tracking Drone (ROS2 + Gazebo)

This project simulates a drone that detects and follows a moving red object using ROS2, Gazebo, and OpenCV.

---

## 📌 Overview

The system works in three steps:

1. Camera captures image from drone  
2. Vision node detects the red object  
3. Control node moves the drone toward the object  

---

## 🧩 Modules

### 1. Simulation
- Drone + camera in Gazebo  
- Moving red object  
- Publishes `/camera/image_raw`  

### 2. Vision
- Detects red object using HSV  
- Finds object center (centroid)  
- Publishes `/object_position` and `/debug_image`  

### 3. Control
- Calculates error from image center  
- Uses proportional control  
- Publishes velocity to drone  

---

## 📡 Topics

- `/camera/image_raw` → camera feed  
- `/object_position` → detected object  
- `/debug_image` → processed image  
- `/X3/gazebo/command/twist` → drone control  

---

## ⚙️ Setup

```bash
cd ~/drone_ws
colcon build
source install/setup.bash
🚀 Run
1. Start simulation
ros2 launch drone_world simulation.launch.py
2. Start vision
ros2 launch drone_vision vision.launch.py
3. Start control
ros2 launch drone_control control.launch.py
🎮 Manual Takeoff
ign topic -t "/X3/gazebo/command/twist" \
-m ignition.msgs.Twist \
-p "linear: {x:0 y:0 z:0.5} angular: {z:0}"
🖥️ View Output
ros2 run rqt_image_view rqt_image_view

Select /debug_image

⚡ Result
Drone detects and follows the red object
Stops when object is not visible
👨‍💻 Authors
Pruthviraj
R Vijay Narasimha Nayak
Prithviraj KC







