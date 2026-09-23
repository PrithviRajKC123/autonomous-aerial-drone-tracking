import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess

def generate_launch_description():
    world_file = os.path.expanduser(
        '~/drone_ws/src/drone_world/worlds/simple_world.sdf'
    )
    model_path = os.path.expanduser(
        '~/drone_ws/src/drone_world/models'
    )

    return LaunchDescription([

        # Start Gazebo
        ExecuteProcess(
            cmd=['bash', '-c',
                 f'export IGN_GAZEBO_RESOURCE_PATH={model_path} && '
                 f'export LIBGL_ALWAYS_SOFTWARE=1 && '
                 f'ign gazebo {world_file} -v 4'],
            output='screen',
            name='gazebo'
        ),

        # Start ROS-Gazebo bridge for camera
        ExecuteProcess(
            cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
                 '/camera/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image'],
            output='screen',
            name='bridge'
        ),

        # Start moving target script
        ExecuteProcess(
            cmd=['python3', os.path.expanduser(
                '~/drone_ws/src/drone_world/scripts/move_target.py')],
            output='screen',
            name='move_target'
        ),

    ])
