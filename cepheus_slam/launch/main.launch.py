import os
import launch
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, PythonExpression,Command
from launch.actions import DeclareLaunchArgument, SetEnvironmentVariable,IncludeLaunchDescription
from launch_ros.actions import Node
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.conditions import IfCondition
import launch_ros
from launch_ros.descriptions import ParameterValue

def generate_launch_description():
    # slam_pkg_share = launch_ros.substitutions.FindPackageShare(package='cepheus_slam').find('cepheus_slam')
    use_sim_time = LaunchConfiguration('use_sim_time')
    slam_launch_dir=os.path.join(get_package_share_directory('cepheus_slam'), 'launch')
    state_launch_dir=os.path.join(get_package_share_directory('cepheus_description'), 'launch')
    gazebo_launch_dir=os.path.join(get_package_share_directory('cepheus_gazebo'), 'launch')

    gazebo_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_launch_dir, 'gazebo.launch.py')),
            condition=IfCondition(use_sim_time),
            launch_arguments={'use_sim_time':use_sim_time}.items())
    
    slam_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(slam_launch_dir, 'carto.launch.py')),
            condition=IfCondition(use_sim_time),
            launch_arguments={'use_sim_time':use_sim_time}.items())
    
    
    state_publisher_launch_cmd=IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(state_launch_dir, 'state_publisher.launch.py')),
            launch_arguments={'use_sim_time':use_sim_time}.items())
   
    
    return launch.LaunchDescription([
        SetEnvironmentVariable('RCUTILS_LOGGING_BUFFERED_STREAM', '1'),
        launch.actions.DeclareLaunchArgument(name='use_sim_time', default_value='True',
                                description='Flag to enable use_sim_time'),
        
        gazebo_launch_cmd,
        state_publisher_launch_cmd,
        slam_launch_cmd
    ])






