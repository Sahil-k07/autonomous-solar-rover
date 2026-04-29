import rclpy
from rclpy.node import Node
from geometry_msgs.msg import Twist
from trajectory_msgs.msg import JointTrajectory, JointTrajectoryPoint
from builtin_interfaces.msg import Duration
import time

class SolarTimedRun(Node):
    def __init__(self):
        super().__init__('solar_timed_run')
        self.vel_pub = self.create_publisher(Twist, '/cmd_vel', 10)
        self.shoulder_pub = self.create_publisher(JointTrajectory, '/shoulder_cmd', 10)
        self.elbow_pub = self.create_publisher(JointTrajectory, '/elbow_cmd', 10)

        # Sequence Format: (Action, Duration_in_Seconds, Speed/Turn_Rate)
        self.sequence = [
            ("ARM_UP", 2.0, 0.0),
            
            # --- PANEL 1 ---
            ("DRIVE", 5.0, 0.5),   # Drive to Panel 1
            ("STOP", 1.0, 0.0),
            ("CLEAN", 6.0, 0.0),   # Execute sweep
            
            # --- BYPASS PANEL 1 ---
            ("BACKUP", 1.5, -0.4), # Reverse slightly
            ("TURN_L", 2.1, 0.5),  # Turn Left 90 degrees
            ("DRIVE", 4.0, 0.5),   # Drive out of the row
            ("TURN_R", 2.1, -0.5), # Turn Right 90 degrees
            ("DRIVE", 8.0, 0.5),   # Drive forward past Panel 1
            ("TURN_R", 2.1, -0.5), # Turn Right 90 degrees
            ("DRIVE", 3.0, 0.5),   # Drive into next row
            ("TURN_L", 2.1, 0.5),  # Turn Left 90 degrees to face Panel 2
            ("STOP", 1.0, 0.0),
            
            # --- PANEL 2 ---
            ("CLEAN", 6.0, 0.0),
            
            # --- BYPASS PANEL 2 ---
            ("BACKUP", 1.5, -0.4),
            ("TURN_L", 2.1, 0.5),
            ("DRIVE", 4.0, 0.5),
            ("TURN_R", 2.1, -0.5),
            ("DRIVE", 8.0, 0.5),
            ("TURN_R", 2.1, -0.5),
            ("DRIVE", 3.0, 0.5),
            ("TURN_L", 2.1, 0.5),
            ("STOP", 1.0, 0.0),
            
            # --- PANEL 3 ---
            ("CLEAN", 6.0, 0.0),
            ("STOP", 1.0, 0.0)
        ]
        
        self.seq_idx = 0
        self.state_start = time.time()
        self.timer = self.create_timer(0.1, self.loop)
        self.get_logger().info("--- INITIATING TIME-BASED AUTONOMY RUN ---")

    def loop(self):
        if self.seq_idx >= len(self.sequence):
            self.vel_pub.publish(Twist())
            self.get_logger().info("EVALUATION COMPLETE.")
            self.timer.cancel()
            return

        action, duration, val = self.sequence[self.seq_idx]
        elapsed = time.time() - self.state_start

        if elapsed >= duration:
            self.seq_idx += 1
            self.state_start = time.time()
            return

        cmd = Twist()
        if action in ["DRIVE", "BACKUP"]:
            cmd.linear.x = val
        elif action in ["TURN_L", "TURN_R"]:
            cmd.angular.z = val
        elif action == "ARM_UP":
            self.move_arm(-0.8, 1.2)
        elif action == "CLEAN":
            if elapsed < 2.0: self.move_arm(0.5, -0.4)
            elif elapsed < 4.0: self.move_arm(0.5, -1.0)
            else: self.move_arm(-0.8, 1.2)
            
        self.vel_pub.publish(cmd)

    def move_arm(self, s, e):
        ts = JointTrajectory(); ts.joint_names = ['arm_shoulder_joint']
        ps = JointTrajectoryPoint(); ps.positions = [float(s)]; ps.time_from_start = Duration(sec=1)
        ts.points.append(ps); self.shoulder_pub.publish(ts)
        te = JointTrajectory(); te.joint_names = ['arm_elbow_joint']
        pe = JointTrajectoryPoint(); pe.positions = [float(e)]; pe.time_from_start = Duration(sec=1)
        te.points.append(pe); self.elbow_pub.publish(te)

def main():
    rclpy.init(); rclpy.spin(SolarTimedRun()); rclpy.shutdown()

if __name__ == '__main__':
    main()