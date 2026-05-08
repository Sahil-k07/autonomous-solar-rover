import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    pkg_dir = get_package_share_directory('solar_rover_description')
    
    # Paths to files
    urdf_file = os.path.join(pkg_dir, 'urdf', 'rover.urdf')
    world_file = os.path.join(pkg_dir, 'worlds', 'solar_farm.world')
    
    # Optional: Path to your saved RViz configuration
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'rover_config.rviz')

    with open(urdf_file, 'r') as infp:
        robot_desc = infp.read()

    # Start robot state publisher
    rsp_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # Start Gazebo and load the custom grass world
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
        launch_arguments={'world': world_file}.items()
    )

    # Spawn the Rover at the origin (0,0) facing Row 2
    # Spawn the Rover at the origin (0,0) facing Row 2
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', 'robot_description', 
            '-entity', 'solar_rover', 
            '-x', '0', '-y', '0', '-z', '0.5',
            '-timeout', '120'  # <-- ADD THIS LINE
        ],
        output='screen'
    )

    # Path to your saved RViz configuration
    rviz_config_file = os.path.join(pkg_dir, 'rviz', 'rover.rviz')

    # Start RViz2 with the saved config
    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file] # This is the magic line that loads your layout!
    )

    return LaunchDescription([
        rsp_node, 
        gazebo, 
        spawn_entity,
        rviz_node
    ])