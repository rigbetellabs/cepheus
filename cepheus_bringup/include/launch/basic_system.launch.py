import os
import time
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument, TimerAction
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    firmware_dir = os.path.join(get_package_share_directory('tortoisebotpro_max_firmware'), 'launch')
    navigation_dir = os.path.join(get_package_share_directory('tortoisebotpro_max_navigation'), 'launch')
    rviz_launch_dir = os.path.join(get_package_share_directory('tortoisebotpro_max_description'), 'launch')
    odom_launch_dir = os.path.join(get_package_share_directory('tortoisebotpro_max_odom'), 'launch')
    ydlidar_launch_dir = os.path.join(get_package_share_directory('ydlidar_ros2_driver'), 'launch')

    # Define each launch file
    state_publisher_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(rviz_launch_dir, 'state_publisher.launch.py')),
        launch_arguments={'use_sim_time': 'False'}.items()
    )

    navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(navigation_dir, 'open_nav_dock.launch.py'))
    )

    rtabmap_odometry_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(odom_launch_dir, 'rtabmap_stereo_odom.launch.py'))
    )

    ydlidar_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(ydlidar_launch_dir, 'ydlidar_launch.py')),
        launch_arguments={'use_sim_time': 'False'}.items()
    )

    microros_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(firmware_dir, 'micro_ros.launch.py'))
    )

    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),

        # Add delays using TimerAction
        TimerAction(period=0.1, actions=[microros_node]),  # Delay of 2 seconds before starting
        TimerAction(period=5.0, actions=[state_publisher_launch_cmd]),  # Delay of 4 seconds
        TimerAction(period=6.0, actions=[ydlidar_launch_cmd]),  # Delay of 6 seconds
        # TimerAction(period=8.0, actions=[navigation_launch_cmd]),  # Uncomment if needed
        # TimerAction(period=10.0, actions=[rtabmap_odometry_launch_cmd]),  # Uncomment if needed
    ])
