# drone_world — Person 1: Simulation Module

## What this package does
- Spawns a quadcopter drone in Gazebo Fortress
- Drone has an onboard camera publishing to /camera/image_raw
- Red target box moves automatically in the world
- Bridges Gazebo camera to ROS2

## Prerequisites
- Ubuntu 22.04
- ROS2 Humble
- Gazebo Fortress v6.16.0
- ros_gz_bridge installed

## Setup (first time only)
```bash
cd ~/drone_ws
colcon build
source install/setup.bash
```

## Launch (single command)
```bash
ros2 launch drone_world simulation.launch.py
```

## Verify it works
Open a new terminal:
```bash
# Check camera topic exists
ros2 topic list | grep camera

# Check camera FPS (should be ~30, minimum 15)
ros2 topic hz /camera/image_raw

# View camera feed
ros2 run rqt_image_view rqt_image_view
# Select /camera/image_raw from dropdown
```

## Topics published
| Topic | Type | Description |
|-------|------|-------------|
| /camera/image_raw | sensor_msgs/Image | Live drone camera feed at 30 FPS |

## Package structure
```
drone_world/
├── models/
│   └── simple_robot/
│       ├── model.sdf       # Drone model with camera
│       └── model.config    # Model metadata
├── worlds/
│   └── simple_world.sdf    # Gazebo world with drone + red box
├── launch/
│   └── simulation.launch.py  # Single launch file
├── scripts/
│   └── move_target.py      # Moves red box automatically
└── README.md
```

## PRD Requirements Met
- FR-01: Gazebo world with ground plane and lighting
- FR-02: Drone spawns at defined pose (x=0, y=0, z=1.5)
- FR-03: Camera publishes at 30 FPS (>= 15 FPS requirement)
- FR-04: Red target box spawned and moving
- FR-05: /camera/image_raw bridged to ROS2
- FR-06: Target object moves via move_target.py script
- AC-01: Full system launches with single command

## Handoff to Person 2 (Vision)
Camera is ready. Subscribe to:
- Topic: /camera/image_raw
- Resolution: 320x240
- FPS: ~30
- Content: Drone view with moving red box visible
