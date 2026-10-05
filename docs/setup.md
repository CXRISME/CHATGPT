# 环境与首次运行（Setup）

本说明以 Ubuntu 22.04 / ROS2 Humble 为暂定基线。尚未在用户实机验证；如果现有镜像不是 Humble，先记录实际环境并选择对应官方文档，不混用发行版（Distribution）。

## 1. 先记录已有环境

电脑与树莓派分别记录以下输出到实验记录：

```bash
cat /etc/os-release
uname -m
printenv ROS_DISTRO
printenv RMW_IMPLEMENTATION
printenv ROS_DOMAIN_ID
```

空的 `RMW_IMPLEMENTATION` 表示未显式指定 ROS 中间件，需记录实际使用实现。另记录树莓派型号、雷达型号、OpenCR 固件版本（能查到时）、电池情况及连接方式。当前仓库没有这些实测信息。

## 2. 电脑端依赖和编译

前提：已按官方文档安装 ROS2 Humble，配置好软件源；下列命令只在匹配的 Ubuntu/ROS2 环境中执行。保留机器人现有镜像。

```bash
sudo apt update
sudo apt install ros-humble-slam-toolbox ros-humble-nav2-map-server ros-humble-tf2-ros ros-humble-rosbag2 ros-humble-rviz2 python3-colcon-common-extensions python3-rosdep
source /opt/ros/humble/setup.bash
```

没有检出仓库时先克隆；已有检出目录则直接进入它：

```bash
git clone https://github.com/CXRISME/CHATGPT.git
cd CHATGPT
```

在根目录执行：

```bash
cp config/robot.env.example config/robot.env
# 编辑 robot.env，确认型号和实验室通信域后加载
source config/robot.env
rosdep update
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select maze_slam_bringup
source install/setup.bash
ros2 launch maze_slam_bringup mapping.launch.py --show-args
```

如果 `rosdep update` 提示尚未初始化，先执行一次 `sudo rosdep init`。每个新终端重新加载 ROS2、工作空间及环境文件。导航依赖在后续阶段安装，本次只需地图保存工具。

## 3. 树莓派驱动与通信

按 ROBOTIS 官方手册中 **Humble** 对应页完成树莓派驱动、雷达与 OpenCR 配置。电脑与树莓派使用匹配的 ROS2 环境、相同通信域，确认网络可通信与时间同步。环境示例可在两端手动设置，不必在树莓派编译本项目。

若硬件确为标准 TurtleBot3 Burger 且驱动已安装，在树莓派终端：

```bash
source /opt/ros/humble/setup.bash
export TURTLEBOT3_MODEL=burger
# ROS_DOMAIN_ID / ROS_LOCALHOST_ONLY 与电脑核实为一致
ros2 launch turtlebot3_bringup robot.launch.py
```

若实验室已有启动方式，先核实它提供的接口，不同时启动两套底盘驱动。

在电脑另一个已加载环境的终端，检查而不发送运动指令：

```bash
ros2 node list
ros2 topic list -t
ros2 topic info /scan --verbose
ros2 topic echo /scan --once
ros2 topic hz /scan
ros2 topic echo /odom --once
ros2 run tf2_ros tf2_echo odom base_footprint
```

`topic hz` 和 `tf2_echo` 持续运行，用 Ctrl+C 退出。记录扫描频率、雷达 frame_id 及时间戳；再检查 `base_footprint` 到实际雷达 frame_id 的 TF。话题或 frame 不同则先修正说明与配置。质量服务（Quality of Service, QoS）不匹配可能导致可见话题却收不到数据，应核对订阅与发布端。

**通过条件：** 收到持续扫描和里程计，TF 链连通，没有持续时间戳／变换错误。未通过时先排查，不继续调 SLAM。

## 4. 首次实机建图

保持机器人驱动运行，在电脑启动：

```bash
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false
```

另一个终端执行 `rviz2`，设置固定坐标系（Fixed Frame）为 `map`，添加 Map、LaserScan 和 TF。Map 显示订阅 `/map`，必要时将持久性（Durability）设为 `Transient Local`。

先原地观察地图和扫描。风险评估（Risk Assessment）获批、现场允许且停机方式确认后，才使用与已装驱动匹配的遥控（Teleoperation）低速移动；本骨架不自动开动机器人。通过走过可识别的墙角、返回起点，观察回环后地图是否合理。

启动建图前可先录制（每次使用新的输出目录）：

```bash
ros2 bag record -o bags/YYYYMMDD_maze01_run01 /scan /odom /tf /tf_static
```

录制完成按 Ctrl+C，执行 `ros2 bag info bags/YYYYMMDD_maze01_run01` 检查实际消息数量、时间范围和静态 TF 是否录入；有录包目录不代表数据有效。仿真录制另加 `--use-sim-time` 并记录 `/clock`。后续回放使用独立会话，停止实机驱动和其他时间源，`ros2 bag play <录包路径> --clock`，SLAM 使用 `use_sim_time:=true`；先确认回放包含所需 TF。

地图已出现时，在仓库根目录另一个终端保存：

```bash
ros2 run nav2_map_server map_saver_cli -f "$PWD/maps/YYYYMMDD_maze01_run01"
```

核实生成的 YAML 和图像配对、图像路径可解析，并查看墙与通道；没有实际保存前，不填写“成功”。复制 `experiments/TEMPLATE.md` 到新的实验记录，填入命令、参数版本、证据和失败原因。

## 官方参考

- [ROS2 Humble 安装](https://docs.ros.org/en/humble/Installation/Ubuntu-Install-Debs.html)
- [TurtleBot3 Bringup：选择 Humble](https://emanual.robotis.com/docs/en/platform/turtlebot3/bringup/)
- [SLAM Toolbox Humble 启动入口](https://github.com/SteveMacenski/slam_toolbox/blob/humble/launch/online_async_launch.py)
- [rosbag2](https://github.com/ros2/rosbag2/tree/humble)
- [Nav2 建图与地图保存](https://docs.nav2.org/tutorials/docs/navigation2_with_slam.html)
