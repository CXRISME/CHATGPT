"""Launch mapping only; robot drivers and transforms must already be available."""

from pathlib import Path

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    slam_share = Path(get_package_share_directory("slam_toolbox"))
    return LaunchDescription([
        DeclareLaunchArgument(
            "use_sim_time",
            default_value="false",
            description="Use /clock for simulation or bag replay; false on real hardware.",
        ),
        DeclareLaunchArgument(
            "slam_params_file",
            default_value=str(slam_share / "config" / "mapper_params_online_async.yaml"),
            description="Absolute path to a complete SLAM Toolbox ROS2 YAML file.",
        ),
        IncludeLaunchDescription(
            PythonLaunchDescriptionSource(
                str(slam_share / "launch" / "online_async_launch.py")
            ),
            launch_arguments={
                "use_sim_time": LaunchConfiguration("use_sim_time"),
                "slam_params_file": LaunchConfiguration("slam_params_file"),
            }.items(),
        ),
    ])
