#!/usr/bin/env python3

import rospy
import actionlib
import sys
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

# Define room coordinates in map frame (from /amcl_pose)
# Format: (pos_x, pos_y, pos_z, or_x, or_y, or_z, or_w)
ROOMS = {
    "patient1": (-1.0511, -9.8156, 0.0, 0.0, 0.0, -0.9425, 0.33401),
    "patient2": (-5.3382, -7.0415, 0.0, 0.0, 0.0, -0.9712, 0.23825),
    "patient3": (-9.2900, -4.8069, 0.0, 0.0, 0.0, -0.8901, 0.4557),
    "patient4": (10.2355, -17.4145, 0.0, 0.0, 0.0, -0.95744, 0.2886),
    "patient5": (4.7628, -14.7372, 0.0, 0.0, 0.0, -0.9076, 0.4196),
    "patient6": (3.1076, -12.2905, 0.0, 0.0, 0.0, 0.9669, 0.255),
    "patient7": (9.8640, -8.8434, 0.0, 0.0, 0.0, -0.2790, 0.96027),
    "loungeroom": (16.925, -20.402, 0.0, 0.0, 0.0, -0.2679, 0.9634),
    "checkroom": (14.05, -6.261, 0.0, 0.0, 0.0, -0.9579, 0.2868),
    "patient8": (21.947, -0.6459, 0.0, 0.0, 0.0, 0.5216, 0.8531),
    "patient9": (19.066, 1.1852, 0.0, 0.0, 0.0, 0.8940, 0.4479),
    "patient10": (13.1821, 3.6330, 0.0, 0.0, 0.0, 0.6169, 0.78702),
    "patient11": (8.7579, 6.6905, 0.0, 0.0, 0.0, 0.54655, 0.83742),
    "patient12": (6.4650, 8.01019, 0.0, 0.0, 0.0, 0.7054, 0.7087),
    "patient13": (0.4732, 11.2813, 0.0, 0.0, 0.0, 0.4023, 0.91546),
    "chamber1": (1.3392, 1.2534, 0.0, 0.0, 0.0, -0.3641, 0.93135),
    "chamber2": (-0.137, -1.6167, 0.0, 0.0, 0.0, 0.05459, 0.9985),
    "centraldesk": (-7.8614, 3.1020, 0.0, 0.0, 0.0, 0.8923, 0.45138)
}

def go_to_room(room_name):
    # Initialize ROS node
    rospy.init_node('go_to_room', anonymous=True)

    # Create a MoveBaseAction client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    client.wait_for_server()

    # Check if room exists
    if room_name not in ROOMS:
        rospy.logerr(f"Room '{room_name}' not defined!")
        return

    # Unpack position and orientation
    pos_x, pos_y, pos_z, or_x, or_y, or_z, or_w = ROOMS[room_name]

    # Define the goal
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    goal.target_pose.pose.position.x = pos_x
    goal.target_pose.pose.position.y = pos_y
    goal.target_pose.pose.position.z = pos_z
    goal.target_pose.pose.orientation.x = or_x
    goal.target_pose.pose.orientation.y = or_y
    goal.target_pose.pose.orientation.z = or_z
    goal.target_pose.pose.orientation.w = or_w

    # Send the goal
    rospy.loginfo(f"Sending goal to {room_name} at ({pos_x}, {pos_y})...")
    client.send_goal(goal)
    client.wait_for_result()

    # Check result
    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo(f"Robot reached {room_name}!")
    else:
        rospy.loginfo(f"Failed to reach {room_name}.")

if __name__ == '__main__':
    try:
        # Default room
        room_name = 'patient1'
        # Parse command-line arguments
        for arg in sys.argv[1:]:
            if arg.startswith('_room:='):
                room_name = arg.split(':=')[1]
                break
        go_to_room(room_name)
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation interrupted.")


"""
#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal

def go_to_room():
    # Initialize ROS node
    rospy.init_node('go_to_room', anonymous=True)

    # Create a MoveBaseAction client
    client = actionlib.SimpleActionClient('move_base', MoveBaseAction)
    
    # Wait for the action server to come up
    rospy.loginfo("Waiting for move_base action server...")
    client.wait_for_server()

    # Define the goal (Room 1 in map frame)
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
    
    # Set position (example: Room 1 at (37.2, 51.8))
    goal.target_pose.pose.position.x = 5.0
    goal.target_pose.pose.position.y = 0.0
    goal.target_pose.pose.position.z = 0.0
    
    # Set orientation (yaw = 0, facing forward)
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 1.0

    # Send the goal
    rospy.loginfo("Sending goal to Room 1 at (5.0, 0.0, 0.0)...")
    client.send_goal(goal)

    # Wait for the robot to reach the goal
    client.wait_for_result()

    # Check if the goal was reached
    if client.get_state() == actionlib.GoalStatus.SUCCEEDED:
        rospy.loginfo("Robot successfully reached Room 1!")
    else:
        rospy.loginfo("Failed to reach Room 1.")

if __name__ == '__main__':
    try:
        go_to_room()
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation interrupted.")
"""