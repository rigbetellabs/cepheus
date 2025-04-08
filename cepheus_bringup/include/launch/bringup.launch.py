import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros
from launch_ros.actions import LifecycleNode
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
  state_publisher_launch_dir=os.path.join(get_package_share_directory('acrux_description'), 'launch')
  firmware_dir = os.path.join(get_package_share_directory('acrux_firmware'), 'launch')
#  x2_params_dir = os.path.join(get_package_share_directory('acrux_firmware'), 'config', 'x2_params.yaml')
  stats_dir = os.path.join(get_package_share_directory('rbl_robot_stats'), 'launch')
  pyserial_dir = os.path.join(get_package_share_directory('acrux_pyserial'), 'launch')
  joy = LaunchConfiguration('joy')
  state_publisher_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(state_publisher_launch_dir, 'state_publisher.launch.py')),)

#  ydlidar_launch_cmd=LifecycleNode(package='ydlidar_ros2_driver',
#                                executable='ydlidar_ros2_driver_node',
#                                name='ydlidar_ros2_driver_node',
#                                output='screen',
#                                emulate_tty=True,
#                                parameters=[x2_params_dir],
#                                namespace='/',
#                                )

  microros_node=launch_ros.actions.Node(
            package='micro_ros_agent',
            executable='micro_ros_agent',
            name='micro_ros_agent',
            arguments=["serial", "--dev", "/dev/esp","-b","921600"]
        )
  realsense_launch=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'realsense_d435i.launch.py')),
        )
  
  hubble_scripts_launch=IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
          os.path.join(firmware_dir, 'hubble_scripts.launch.py')),
        )
  auto_joy_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'auto_joy_teleop.launch.py')),
        condition=IfCondition(joy),
    )

  stats_node = IncludeLaunchDescription(
    PythonLaunchDescriptionSource(
        os.path.join(stats_dir, 'robot_stats.launch.py')),
   )
  
  rplidar_launch=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'rplidar_a3.launch.py')),
        )

  pyserial_node = IncludeLaunchDescription(
      PythonLaunchDescriptionSource(
          os.path.join(pyserial_dir, 'pyserial_to_ros2.launch.py')),
      )

  bump_sensing_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'ultrasonic_bump_sensing.launch.py')),
        )

  return LaunchDescription([

    SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
    DeclareLaunchArgument(name='joy', default_value='True',
                                              description='To enable joystick control'),

    state_publisher_launch_cmd,
#    ydlidar_launch_cmd,
#    realsense_launch, 
    microros_node, 
    hubble_scripts_launch,
    auto_joy_cmd,
    stats_node,
    rplidar_launch,
    pyserial_node,
    bump_sensing_node

  ]
)

