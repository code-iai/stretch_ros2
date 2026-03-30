import os

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, EnvironmentVariable, PathJoinSubstitution
from ament_index_python.packages import get_package_share_directory


def generate_launch_description():
    # Package share directories
    stretch_nav2_dir = get_package_share_directory('stretch_nav2')
    stretch_core_dir = get_package_share_directory('stretch_core')

    # Arguments
    map_arg = DeclareLaunchArgument(
        'map',
        default_value=PathJoinSubstitution([
            EnvironmentVariable('HELLO_FLEET_PATH'),
            'maps',
            'apartment.yaml'
        ]),
        description='Full path to the map.yaml file to use for navigation'
    )

    use_rviz_arg = DeclareLaunchArgument(
        'use_rviz',
        default_value='false',
        description='Whether to launch RViz'
    )

    # Navigation stack + driver (stretch_nav2/navigation.launch.py)
    navigation_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(stretch_nav2_dir, 'launch', 'navigation.launch.py')
        ),
        launch_arguments={
            'map': LaunchConfiguration('map'),
            'use_rviz': LaunchConfiguration('use_rviz')
        }.items()
    )

    # Head camera (D435i, low resolution)
    head_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(stretch_core_dir, 'launch', 'd435i_low_resolution.launch.py')
        )
    )

    # Hand camera (D405 basic)
    hand_camera_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(stretch_core_dir, 'launch', 'd405_basic.launch.py')
        )
    )

    return LaunchDescription([
        map_arg,
        use_rviz_arg,
        navigation_launch,
        head_camera_launch,
        hand_camera_launch,
    ])