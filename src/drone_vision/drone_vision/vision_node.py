#!/usr/bin/env python3

import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
import cv2
import numpy as np

class VisionNode(Node):
    def __init__(self):
        super().__init__('vision_node')

        self.bridge = CvBridge()

        self.sub = self.create_subscription(
            Image, '/camera/image_raw', self.image_callback, 10)

        self.pos_pub = self.create_publisher(Point, '/object_position', 10)
        self.debug_pub = self.create_publisher(Image, '/debug_image', 10)

        # HSV thresholds — wide range for dark red
        self.lower_red1 = np.array([0,   30, 20])
        self.upper_red1 = np.array([15,  255, 255])
        self.lower_red2 = np.array([155, 30, 20])
        self.upper_red2 = np.array([180, 255, 255])

        self.get_logger().info('Vision node started!')

    def image_callback(self, msg):
        frame = self.bridge.imgmsg_to_cv2(msg, 'bgr8')
        hsv   = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

        mask1 = cv2.inRange(hsv, self.lower_red1, self.upper_red1)
        mask2 = cv2.inRange(hsv, self.lower_red2, self.upper_red2)
        mask  = cv2.bitwise_or(mask1, mask2)
        mask  = cv2.medianBlur(mask, 5)

        contours, _ = cv2.findContours(
            mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        point = Point()
        detected = False

        if contours:
            c    = max(contours, key=cv2.contourArea)
            area = cv2.contourArea(c)

            if area > 200:  # lowered from 1500
                M = cv2.moments(c)
                if M['m00'] != 0:
                    cx = int(M['m10'] / M['m00'])
                    cy = int(M['m01'] / M['m00'])

                    point.x = float(cx)
                    point.y = float(cy)
                    point.z = 0.0
                    detected = True

                    x, y, w, h = cv2.boundingRect(c)
                    cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)
                    cv2.circle(frame, (cx, cy), 5, (0, 255, 0), -1)
                    cv2.putText(frame, f'({cx},{cy})', (cx+10, cy),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,255,0), 1)

                    self.get_logger().info(
                        f'Detected cx={cx} cy={cy} area={area:.0f}')

        if not detected:
            point.z = -1.0
            cv2.putText(frame, 'NO OBJECT DETECTED', (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,0,255), 2)

        h, w = frame.shape[:2]
        cv2.circle(frame, (w//2, h//2), 5, (255, 0, 0), -1)

        self.pos_pub.publish(point)
        self.debug_pub.publish(self.bridge.cv2_to_imgmsg(frame, 'bgr8'))

def main():
    rclpy.init()
    node = VisionNode()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
