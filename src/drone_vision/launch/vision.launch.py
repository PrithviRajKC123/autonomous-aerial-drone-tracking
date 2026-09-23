from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='drone_vision',
            executable='vision_node',
            name='vision_node',
            parameters=['/home/pes2ug23cs452/drone_ws/src/drone_vision/config/color_params.yaml']
        )
    ])
