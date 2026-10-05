# 配置说明（Configuration）

本目录存放环境示例及后续已验证的 SLAM 参数。`robot.env.example` 不会自动生效，必须复制为 `robot.env`、核实后在每个终端加载。

| 配置项 | 含义与核实方式 |
| --- | --- |
| `TURTLEBOT3_MODEL=burger` | 机器人模型；与实际硬件一致 |
| `ROS_DOMAIN_ID=30` | ROS2 通信域（Domain）；30 是示例，两端一致并避免实验室其他机器人 |
| `ROS_LOCALHOST_ONLY=0` | 允许非本机发现；仍需检查网络、防火墙和中间件（Middleware） |
| `use_sim_time` | 实机 `false`；仿真或带 `/clock` 的回放用 `true`；相关节点保持一致 |
| `slam_params_file` | SLAM Toolbox 完整 YAML 参数文件的绝对路径 |

启动包默认使用**当前安装版本** SLAM Toolbox 的 `mapper_params_online_async.yaml`，避免复制不匹配版本的一套参数。上游 Humble 配置常用 `map`、`odom`、`base_footprint` 和 `/scan`，必须以现场 TF 与话题为准。

## 固化第一个基线

在仓库根目录、已加载 ROS2 环境的终端执行：

```bash
cp "$(ros2 pkg prefix --share slam_toolbox)/config/mapper_params_online_async.yaml" config/slam_baseline.yaml
```

核实其中 `slam_toolbox.ros__parameters` 下的 `mode: mapping`、`scan_topic`、`base_frame`、`odom_frame`、`map_frame`；雷达量程依据实际传感器设置。保留完整文件，包括求解器（Solver）参数。启动时：

```bash
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false slam_params_file:="$PWD/config/slam_baseline.yaml"
```

保存来源版本：`dpkg-query -W ros-humble-slam-toolbox`，提交该 YAML 并在实验记录填写 SHA。可用 `ros2 param dump /slam_toolbox` 检查运行时参数，与文件对照；时间源以 launch 参数为准。

先建立基线，再每次只改一个变量，如地图分辨率（Map Resolution）、最小移动距离或回环检测（Loop Closure）阈值。记录原值、新值、原因和结果，不把上游默认值写成“已优化”。

## TF 与时间

- 机器人驱动提供 `odom → base_footprint`，机器人描述提供到激光坐标系的变换；SLAM 提供 `map → odom`。
- 具体底盘／雷达坐标系以 `/scan.header.frame_id` 与 TF 树为准，不能通过乱加静态变换掩盖缺失的驱动。
- 之后使用自适应蒙特卡洛定位（Adaptive Monte Carlo Localisation, AMCL）时，由 AMCL 提供 `map → odom`；关闭建图 SLAM，避免两个节点争用同一变换。
- 实机电脑和树莓派需同步系统时间；仿真与回放需有有效 `/clock`。

上游启动与配置参考：[SLAM Toolbox Humble](https://github.com/SteveMacenski/slam_toolbox/tree/humble)。
