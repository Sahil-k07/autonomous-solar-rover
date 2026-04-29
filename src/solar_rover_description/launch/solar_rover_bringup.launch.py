import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # 1. Setup paths
    pkg_description = get_package_share_directory('solar_rover_description')
    pkg_gazebo_ros = get_package_share_directory('gazebo_ros')
    
    urdf_path = os.path.join(pkg_description, 'urdf', 'rover.urdf')
    
    # Read the URDF file
    with open(urdf_path, 'r') as infp:
        robot_desc = infp.read()

    # 2. Define the Robot State Publisher node
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_desc}]
    )

    # 3. Define the Gazebo launch (Fixed syntax here)
    # Find the project package
    pkg_project = get_package_share_directory('project')
    world_file = os.path.join(pkg_project, 'solar_farm_mega.sdf')

    # Launch Gazebo with the world file
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            os.path.join(pkg_gazebo_ros, 'launch', 'gazebo.launch.py')
        ]),
        launch_arguments={'world': world_file}.items()
    )

    # 4. Define the Spawn node
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-topic', 'robot_description', '-entity', 'solar_rover'],
        output='screen'
    )

    # 5. Return the LaunchDescription object
    return LaunchDescription([
        robot_state_publisher,
        gazebo,
        spawn_robot
    ])