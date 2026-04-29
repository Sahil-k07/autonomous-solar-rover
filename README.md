# Autonomous Solar Panel Cleaning Rover (ROS 2 & Gazebo)

A fully simulated autonomous robotics project built with **ROS 2 (Humble)** and **Gazebo**. This repository contains the custom URDF, 3D meshes, simulated environments, and Python-based autonomy scripts for a 6-wheeled skid-steer rover designed to navigate and clean solar farm installations.

## 🛠️ Tech Stack
* **Framework:** ROS 2 (Humble Hawksbill)
* **Simulation:** Gazebo
* **Languages:** Python, XML (URDF/SDF)
* **Key Plugins:** `libgazebo_ros_diff_drive.so`, `libgazebo_ros_joint_pose_trajectory.so`, `libgazebo_ros_ray_sensor.so`

## ⚙️ Core Features
* **Custom 6-Wheel Skid-Steer Kinematics:** Tuned lateral friction (`mu1`, `mu2`) parameters within Gazebo to allow smooth skid-steering without odometry drift or physics locking.
* **3-DOF Robotic Manipulator:** A shoulder, elbow, and continuous wrist joint assembly equipped with a cleaning brush, controlled via PID joint trajectory controllers.
* **Primitive Collision Optimization:** To prevent physics interpenetration (simulation explosions) caused by complex `.stl` files, the URDF utilizes lightweight geometric primitives for collision calculations while retaining high-fidelity meshes for visual rendering.
* **Time-Based Dead Reckoning Autonomy:** A Python state machine that executes a flawless sequence of driving, deploying the arm, cleaning, and executing complex bypass maneuvers to navigate from panel to panel.
* **Teleop Ready:** Fully compatible with `teleop_twist_keyboard` for manual override and control.

## 🚀 How to Run

**1. Clone the repository and build the workspace:**
```bash

git clone [https://github.com/YOUR-USERNAME/autonomous-solar-rover-ros2.git](https://github.com/YOUR-USERNAME/autonomous-solar-rover-ros2.git)
cd autonomous-solar-rover-ros2
colcon build --symlink-install
source install/setup.bash

**2. Launch the Gazebo Simulation:**

ros2 launch solar_rover_description solar_rover_bringup.launch.py gui:=false
(In a separate terminal, run gzclient --verbose to open the visualizer).

**3. Run the Autonomy Script:**

ros2 run project autonomy_eval

**4. (Optional) Manual Control:**

ros2 run teleop_twist_keyboard teleop_twist_keyboard