from launch import LaunchDescription
from launch_ros.actions import Node

def generate_launch_description():
    return LaunchDescription([
        Node(
            package='drone_control',
            executable='control_node',
            name='control_node',
            output='screen',
            parameters=[{
                'kp_yaw': 0.005,
                'kp_fwd': 0.008,
            }]
        )
    ])
