# Drone Vision Module (Person 2)

## Overview

This package implements the vision system for the Aerial Object Tracking project.

It processes the drone camera feed and detects a red object using HSV color filtering.
The system publishes the detected object position and a debug image for visualization.

---

## Features

* Subscribes to `/camera/image_raw`
* Detects red object using HSV color thresholding
* Computes centroid of detected object
* Publishes position to `/object_position`
* Publishes annotated image to `/debug_image`
* Handles no-detection case (`z = -1`)
* Configurable HSV thresholds via YAML

---

## Topics

| Topic               | Type                | Description            |
| ------------------- | ------------------- | ---------------------- |
| `/camera/image_raw` | sensor_msgs/Image   | Input camera feed      |
| `/object_position`  | geometry_msgs/Point | Object centroid        |
| `/debug_image`      | sensor_msgs/Image   | Annotated output image |

---

## Output Format

* `x`, `y` → pixel coordinates of object center
* `z = 0.0` → object detected
* `z = -1.0` → no object detected

---

## Setup

```bash
cd ~/drone_ws
colcon build
source install/setup.bash
```

---

## Run

### 1. Start simulation

```bash
ros2 launch drone_world simulation.launch.py
```

### 2. Start vision node

```bash
ros2 launch drone_vision vision.launch.py
```

---

## Debug Visualization

```bash
ros2 run rqt_image_view rqt_image_view
```

Select:

```
/debug_image
```

---

## Configuration

HSV thresholds are configurable via:

```
config/color_params.yaml
```

Example:

```yaml
lower_red1: [0, 150, 100]
upper_red1: [10, 255, 255]
```

---

## Performance

* Frame rate: ~25 FPS
* Low latency real-time detection
* Stable tracking of moving object

---

## Notes

* Detection is based on color; lighting conditions may affect results
* System is designed for single-object tracking (red target only)

---

## Status

✔ Fully implemented as per PRD (FR-07 to FR-13)
✔ Tested and validated in simulation
