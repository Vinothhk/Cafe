# BUTLER BOT in CAFE



## TITLE & ABOUT
- The ButlerBot project aims to develop an autonomous robot capable of delivering orders from the kitchen to specific tables in a cafe. 
- used a differential drive robot
- This project is built on ROS 2 Humble (Ubuntu 22.04)
[image](https://github.com/noshluk2/ROS2-Autonomous-Driving-and-Navigation-SLAM-with-TurtleBot3/blob/master/image_resources/main_cover.png)
## HOW TO INSTALL
Create workspace
```bash
mkdir -p ros2_ws/src
cd ros2_ws/src
```
clone this repository
```bash
git clone https://github.com/Vinothhk/Cafe.git
```
Build the workspace
```bash
cd ..
colcon build
source install/setup.bash
```
## USAGE
To spawn the robot in gazebo and visualize:
```bash
ros2 launch butlerbot spawn_robots.launch.xml
```
To perform mapping (SLAM):
```bash
ros2 launch butlerbot slam.launch.py use_sim_time:=true
```
To bringup all the navigation nodes along with gazebo simulation:
```bash
ros2 launch butlerbot navigation.launch.xml
```

## APPROACH

## Run the CODE
