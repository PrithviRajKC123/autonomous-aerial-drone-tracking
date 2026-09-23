#!/usr/bin/env python3

import subprocess
import math
import time

t = 0.0
print("Move target started!")

while True:
    t += 0.05
    x = 2.0 + math.sin(t * 0.3) * 1.5
    y = math.sin(t * 0.6) * 1.0
    z = 0.5

    cmd = f'''ign service -s /world/simple_world/set_pose --reqtype ignition.msgs.Pose --reptype ignition.msgs.Boolean --timeout 300 --req 'name: "red_box", position: {{x: {x}, y: {y}, z: {z}}}\''''

    subprocess.Popen(cmd, shell=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    print(f"Target at x={x:.2f} y={y:.2f}")
    time.sleep(0.1)
