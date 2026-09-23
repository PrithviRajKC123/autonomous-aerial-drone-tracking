import os
from launch import LaunchDescription
from launch.actions import ExecuteProcess, TimerAction
from launch_ros.actions import Node

def generate_launch_description():
    world_file = os.path.expanduser(
        '~/drone_ws/src/drone_world/worlds/simple_world.sdf'
    )
    model_path = os.path.expanduser(
        '~/drone_ws/src/drone_world/models'
    )

    return LaunchDescription([

        # 1. Start Gazebo
        ExecuteProcess(
            cmd=['bash', '-c',
                 f'export IGN_GAZEBO_RESOURCE_PATH={model_path} && '
                 f'export LIBGL_ALWAYS_SOFTWARE=1 && '
                 f'ign gazebo {world_file} -v 4'],
            output='screen',
            name='gazebo'
        ),

        # 2. Start bridge after 5 seconds
        TimerAction(period=5.0, actions=[
            ExecuteProcess(
                cmd=['ros2', 'run', 'ros_gz_bridge', 'parameter_bridge',
                     '/camera/image_raw@sensor_msgs/msg/Image@ignition.msgs.Image',
                     '/X3/gazebo/command/twist@geometry_msgs/msg/Twist@ignition.msgs.Twist',
                     '/model/x3/odometry@nav_msgs/msg/Odometry@ignition.msgs.Odometry'],
                output='screen',
                name='bridge'
            ),
        ]),

        # 3. Start vision node after 6 seconds
        TimerAction(period=6.0, actions=[
            Node(
                package='drone_vision',
                executable='vision_node',
                name='vision_node',
                output='screen',
            ),
        ]),

        # 4. Start moving target after 7 seconds
        TimerAction(period=7.0, actions=[
            ExecuteProcess(
                cmd=['python3', os.path.expanduser(
                    '~/drone_ws/src/drone_world/scripts/move_target.py')],
                output='screen',
                name='move_target'
            ),
        ]),

        # NOTE: Control node is started MANUALLY after lifting drone
        # Command: ros2 launch drone_control control.launch.py

    ])
