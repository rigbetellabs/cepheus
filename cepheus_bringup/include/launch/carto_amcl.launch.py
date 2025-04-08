import os
from launch import LaunchDescription
from launch.actions import SetEnvironmentVariable, IncludeLaunchDescription, DeclareLaunchArgument
from launch.conditions import IfCondition
from launch.substitutions import LaunchConfiguration, PythonExpression
from launch.launch_description_sources import PythonLaunchDescriptionSource
import launch_ros
from launch_ros.actions import LifecycleNode
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    firmware_dir = os.path.join(get_package_share_directory('acrux_firmware'), 'launch')
    navigation_dir = os.path.join(get_package_share_directory('acrux_navigation'), 'launch')
    rviz_launch_dir = os.path.join(get_package_share_directory('acrux_description'), 'launch')
    gazebo_launch_dir = os.path.join(get_package_share_directory('acrux_gazebo'), 'launch')
    cartographer_launch_dir = os.path.join(get_package_share_directory('acrux_slam'), 'launch')
    stats_dir = os.path.join(get_package_share_directory('rbl_robot_stats'), 'launch')
    pyserial_dir = os.path.join(get_package_share_directory('acrux_pyserial'), 'launch')
    voyage_dir = os.path.join(get_package_share_directory('acrux_voyager'), 'launch')
    map_directory = os.path.join(get_package_share_directory('acrux_navigation'), 'maps', 'room2.yaml')
    rviz_config_path = os.path.join(get_package_share_directory('acrux_description'), 'rviz/navigation.rviz')
    x2_params_dir = os.path.join(get_package_share_directory('acrux_firmware'), 'config', 'x2_params.yaml')
    pf_dir = os.path.join(get_package_share_directory('pf_driver'), 'launch')

    map_file = LaunchConfiguration('map_file')
    use_sim_time = LaunchConfiguration('use_sim_time')
    exploration = LaunchConfiguration('exploration')
    realsense = LaunchConfiguration('realsense')
    merge_scan = LaunchConfiguration('merge_scan')
    joy = LaunchConfiguration('joy')

    rviz_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rviz_launch_dir, 'rviz.launch.py')),
        condition=IfCondition(use_sim_time),
        launch_arguments={'use_sim_time': use_sim_time,
                          "rvizconfig": rviz_config_path}.items())

    state_publisher_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(rviz_launch_dir, 'state_publisher.launch.py')),
        launch_arguments={'use_sim_time': use_sim_time}.items())

    gazebo_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_launch_dir, 'gazebo.launch.py')),
        condition=IfCondition(use_sim_time),
        launch_arguments={'use_sim_time': use_sim_time}.items())

    navigation_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(navigation_dir, 'amcl_navigation.launch.py')),
        launch_arguments={'exploration': exploration,
                          'map_file': map_file,
                          'use_sim_time': 'False'}.items())

    cartographer_launch_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(cartographer_launch_dir, 'cartographer.launch.py')),
        launch_arguments={'exploration': exploration,
                          'use_sim_time': use_sim_time}.items())

    only_ydlidar_launch_cmd = LifecycleNode(package='ydlidar_ros2_driver',
                                executable='ydlidar_ros2_driver_node',
                                name='ydlidar_ros2_driver_node',
                                condition=IfCondition(PythonExpression(["not ", use_sim_time, " and not ", merge_scan])),
                                output='screen',
                                emulate_tty=True,
                                parameters=[x2_params_dir],
                                namespace='/',
                                )

    remapped_ydlidar_launch_cmd = LifecycleNode(package='ydlidar_ros2_driver',
                                executable='ydlidar_ros2_driver_node',
                                name='ydlidar_ros2_driver_node',
                                remappings=[('scan', '/lidar/scan')],
                                condition=IfCondition(PythonExpression(["not ", use_sim_time, " and ", merge_scan])),
                                output='screen',
                                emulate_tty=True,
                                parameters=[x2_params_dir],
                                namespace='/',
                                )
    
    rplidar_launch=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'rplidar_a3.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))

    pf_launch=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'r2000_merge.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))
    
    microros_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'micro_ros.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))

    hubble_scripts_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'hubble_scripts.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))

    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'realsense_d435i.launch.py')),
        condition=IfCondition(
            PythonExpression(["not ", use_sim_time, " and ", realsense])
        ))
    merged_scan_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'merge_scan.launch.py')),
        condition=IfCondition(merge_scan),
        )

    auto_joy_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'auto_joy_teleop.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time, " and ", joy])),
    )
    
    stats_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(stats_dir, 'robot_stats.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))
    
    pyserial_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pyserial_dir, 'pyserial_to_ros2.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))
    
    bump_sensing_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(firmware_dir, 'ultrasonic_bump_sensing.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))
    
    voyage_node = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(voyage_dir, 'start_voyage.launch.py')),
        condition=IfCondition(PythonExpression(["not ", use_sim_time])))    

    return LaunchDescription([
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
        DeclareLaunchArgument(name='use_sim_time', default_value='False',
                                             description='Flag to enable use_sim_time'),
        DeclareLaunchArgument(name='exploration', default_value='False',
                                             description='Flag to enable exploration'),
        DeclareLaunchArgument(name='map_file', default_value=map_directory,
                                              description='Map to be used'),
        DeclareLaunchArgument(name='realsense', default_value='False',
                                              description='Realsense to be used'),
        DeclareLaunchArgument(name='merge_scan', default_value='False',
                                              description='To merge scan or not'),
        DeclareLaunchArgument(name='joy', default_value='True',
                                              description='To enable joystick control'),

        # rviz_launch_cmd,
        state_publisher_launch_cmd,
        # only_ydlidar_launch_cmd,
        # remapped_ydlidar_launch_cmd,
        rplidar_launch,
        realsense_launch,
        gazebo_launch_cmd,
        navigation_launch_cmd,
        cartographer_launch_cmd,
        microros_node,
        hubble_scripts_launch,
        merged_scan_launch,
        auto_joy_cmd,
        pyserial_node,
        stats_node,
        bump_sensing_node,
        voyage_node,
        pf_launch

    ])

