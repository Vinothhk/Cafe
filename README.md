# BUTLER BOT in CAFE



## TITLE & ABOUT
- The ButlerBot project aims to develop an autonomous robot capable of delivering orders from the kitchen to specific tables in a cafe. 
- used a differential drive robot
- This project is built on ROS 2 Humble (Ubuntu 22.04)
 ![alt text](https://github.com/Vinothhk/Cafe/blob/main/butlerbot/images/image.png)

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
- Move Robot Node Initialized
#### ACTION CLIENT
- An Action Client for **NavigatetoPose** action is created, which is responsible for sending navigation goals to the robot.
#### ORDER HANDLING
- The _process_ method handles the main logic of interacting with the user, taking orders, confirming deliveries, and handling cancellations.
- User input is taken to determine if an order is to be placed.
- If an order is placed, the table numbers are collected, and the robot is instructed to move to the kitchen to pick up the order.
- Once the kitchen confirms that the order is ready, the robot proceeds to deliver the order to the specified tables.
- The user is asked for confirmation at each table, and the order is marked as delivered if confirmed.
- The robot moves to home after successful deliveries of orders.
- If any of the order get cancelled or the the customer fail to attend the robot at the table, it then moves to kitchen before returning to Home. 
#### NAVIGATION FUNCTIONS
- The methods _move_to_kitchen_, _move_to_tableone_, _move_to_tabletwo_, _move_to_tablethree_, and _move_to_home_ are used to move the robot to specific locations.
- These methods call the _move_to_position_ method with the coordinates of the target location.
#### FEEDBACK & RESULT HANDLING
- The _goal_response_callback_ method handles the response from the action server, checking if the goal was accepted.
- The __wait_for_result_ method waits for the action server to complete the goal and logs the result.

## RUN THE CODE
We need a couple of terminals to execute the program successfully.

In Terminal 1:
```bash
ros2 launch butlerbot navigation.launch.xml
```

In RViz, click on 'Open Config' and load the 'nav.rviz' from butlerbot/config/.
Wait a couple of seconds for the robot to take pose.

In Terminal 2:
Let's run the main script..
```bash
ros2 run butlerbot move_robot.py
```

Now you can interact with the Spinning node through Terminal 2!!

(Pic of Running Program)

 ![alt text](https://github.com/Vinothhk/Cafe/blob/main/butlerbot/images/Screenshot%20from%202024-07-06%2008-52-33.png)
