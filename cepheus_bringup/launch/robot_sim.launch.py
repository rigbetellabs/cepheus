import os
import time
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    navigation_dir = os.path.join(get_package_share_directory('cepheus_navigation'), 'launch')
    rviz_launch_dir = os.path.join(get_package_share_directory('cepheus_description'), 'launch')
    gazebo_launch_dir = os.path.join(get_package_share_directory('cepheus_description'), 'launch')

    # Define each launch file
    state_publisher_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rviz_launch_dir, 'state_publisher.launch.py')),
        launch_arguments={'use_sim_time': 'True'}.items()
    )

    navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(navigation_dir, 'nav3.launch.py')),
        launch_arguments={'use_sim_time': 'True'}.items()
    )


    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(gazebo_launch_dir, 'gazebo.launch.py'))
    )



    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),

        # Add delays using TimerAction# Delay of 2 seconds before starting
        TimerAction(period=1.0, actions=[state_publisher_launch_cmd]),  # Delay of 4 seconds
        TimerAction(period=2.0, actions=[gazebo_launch_cmd]),  # Delay of 6 seconds
        TimerAction(period=5.0, actions=[navigation_launch_cmd]),  # Uncomment if needed
    ])
