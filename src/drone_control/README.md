# drone_control — Person 3: Control Module

## What this package does
- Subscribes to /object_position from vision node
- Calculates error from image center
- Publishes velocity commands to /X3/gazebo/command/twist
- Drone autonomously follows detected red object
- Stops drone when object not detected

## PRD Requirements Met
- FR-14: Subscribes to /object_position
- FR-15: Proportional control — velocity = Kp x error
- FR-16: Velocity clamped to safe limits (±0.5 rad/s, ±0.3 m/s)
- FR-17: Publishes at 10 Hz
- FR-18: Stops drone when z=-1.0 (no detection)
- FR-19: Kp gains tunable via ROS2 parameters

## Topics
| Topic | Type | Direction |
|-------|------|-----------|
| /object_position | geometry_msgs/Point | Subscribed |
| /X3/gazebo/command/twist | geometry_msgs/Twist | Published |

## Control Logic
error_x = 160 - cx   (image center - object x)
error_y = 120 - cy   (image center - object y)
angular.z = Kp_yaw x error_x
linear.x  = -Kp_fwd x error_y

## Run
```bash
ros2 launch drone_control control.launch.py
```

## Tune gains live
```bash
ros2 param set /control_node kp_yaw 0.005
ros2 param set /control_node kp_fwd 0.008
```
