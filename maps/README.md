# 地图（Maps）

命名：`YYYYMMDD_maze01_run01.yaml` 与同名 `.pgm`／实际输出图像格式。提交时成对保存，核实 YAML 的 `image` 路径；相对路径应能在另一台电脑解析。小型地图可纳入 Git，大图只提交索引。

在对应实验记录写明地图来源的代码 SHA、SLAM 参数、环境尺寸、录包及质量检查。新实验保存新名字，避免覆盖旧地图。

占据栅格（Occupancy Grid）地图供后续 Nav2 使用；它不等于 SLAM 的位姿图（Pose Graph）。若要继续优化或续建，另按 SLAM Toolbox 序列化（Serialization）接口保存位姿图并记录软件版本。当前未生成任何地图。
