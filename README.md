# CHATGPT

## ROS2 SLAM / FYP 最小项目骨架

目标：使用基于树莓派（Raspberry Pi）的 TurtleBot3 Burger，扫描真实迷宫，完成同步定位与建图（Simultaneous Localisation and Mapping, SLAM），再基于地图定位并规划、执行路线。

**当前状态：项目骨架。** 提供文档、实验模板和 SLAM 启动入口；尚无实机建图、定位或导航的验证结果。导航（Navigation）是后续阶段，建图成功不代表已实现自主导航或自主探索（Autonomous Exploration）。

暂定复现基线：Ubuntu 22.04 + ROS2 Humble；机器人型号采用 Burger。实际电脑/树莓派系统、激光雷达（LiDAR）型号、固件与话题名仍需核实，不要为了匹配示例重装现有设备。

### 文件入口

| 路径 | 用途 |
| --- | --- |
| [docs/setup.md](docs/setup.md) | 环境确认、依赖、编译、连接与首次建图 |
| [config/README.md](config/README.md) | 配置项、时间源、坐标系和调参记录 |
| [config/robot.env.example](config/robot.env.example) | 不含地址或凭据的环境变量示例 |
| [src/maze_slam_bringup](src/maze_slam_bringup) | 自定义 ROS2 启动包（Bringup Package） |
| [experiments/TEMPLATE.md](experiments/TEMPLATE.md) | 可复现实验记录模板 |
| [maps/README.md](maps/README.md) | 地图文件和版本约定 |
| [bags/README.md](bags/README.md) | rosbag2 数据录包约定 |
| [docs/next-steps.md](docs/next-steps.md) | 分阶段开发任务和验收条件 |

### 从哪里开始

1. 按 [环境说明](docs/setup.md) 核实两端系统、ROS2 版本和雷达；先完成 `/scan`、里程计（Odometry）和坐标变换（TF）检查。
2. 安装依赖并用 `colcon` 编译本仓库。它可以直接作为工作空间（Workspace）根目录。
3. 在已启动机器人驱动、TF 正常的前提下，在电脑运行：

```bash
source /opt/ros/humble/setup.bash
source install/setup.bash
source config/robot.env
ros2 launch maze_slam_bringup mapping.launch.py use_sim_time:=false
```

`robot.env` 必须先由示例复制并确认，见环境说明。启动入口只运行 SLAM Toolbox，不启动底盘驱动、不发布运动指令，也不启动 Nav2。

4. 复制实验模板，记录首个实验，再保存地图与证据。下一阶段依次是地图定位、路径规划（Path Planning）和自主导航（Autonomous Navigation）。

### 提交约定

- 一次提交（Commit）对应一个可说明的改动；实验记录注明代码提交 SHA、参数文件及数据来源。
- `build/`、`install/`、`log/`、本机环境文件与录包不会默认提交。小地图可以提交；大文件只记录可访问位置、大小及校验值。
- 使用分支与拉取请求（Pull Request, PR）审阅变更，保留失败实验及原因。
- 本次扩展保留原 README 标题与原始提交历史。开源许可尚未决定，`package.xml` 的 `TODO` 需在对外授权复用前补齐。
