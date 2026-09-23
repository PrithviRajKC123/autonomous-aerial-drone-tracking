#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Point, Twist

IMAGE_W = 320
IMAGE_H = 240

class ControlNode(Node):
    def __init__(self):
        super().__init__("control_node")
        self.declare_parameter("kp_yaw", 0.005)
        self.declare_parameter("kp_fwd", 0.008)
        self.MAX_ANG = 0.5
        self.MAX_LIN = 0.3
        self.obj_x = 0.0
        self.obj_y = 0.0
        self.detected = False
        self.sub = self.create_subscription(Point, "/object_position", self.position_callback, 10)
        self.pub = self.create_publisher(Twist, "/X3/gazebo/command/twist", 10)
        self.timer = self.create_timer(0.1, self.control_loop)
        self.get_logger().info("Control node started!")

    def position_callback(self, msg):
        if msg.z == -1.0:
            self.detected = False
        else:
            self.detected = True
            self.obj_x = msg.x
            self.obj_y = msg.y

    def clamp(self, val, min_val, max_val):
        return max(min_val, min(max_val, val))

    def control_loop(self):
        cmd = Twist()
        kp_yaw = self.get_parameter("kp_yaw").value
        kp_fwd = self.get_parameter("kp_fwd").value
        if self.detected:
            error_x = IMAGE_W / 2 - self.obj_x
            error_y = IMAGE_H / 2 - self.obj_y
            cmd.angular.z = self.clamp(kp_yaw * error_x, -self.MAX_ANG, self.MAX_ANG)
            cmd.linear.x = self.clamp(kp_fwd * error_y, -self.MAX_LIN, self.MAX_LIN)
            self.get_logger().info(f"Tracking: ex={error_x:.1f} ey={error_y:.1f} ang={cmd.angular.z:.3f} lin={cmd.linear.x:.3f}")
        else:
            self.get_logger().info("No object - hovering")
        self.pub.publish(cmd)

def main():
    rclpy.init()
    node = ControlNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == "__main__":
    main()
