#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from turtlesim.msg import Pose
from math import atan2

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.x
    y = msg.y
    theta = msg.theta

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/turtlesim1/turtle1/pose", Pose, newOdom)
pub = rospy.Publisher("/turtlesim1/turtle1/cmd_vel", Twist, queue_size=1)
r = rospy.Rate(4)
turtle_vel = Twist()
goal_x = 10
goal_y = 10
t0 = rospy.Time.now().to_sec()
while not rospy.is_shutdown():
    t1 = rospy.Time.now().to_sec()
    inc_x = goal_x -x
    inc_y = goal_y -y

    angle_to_goal = atan2(inc_y, inc_x)

    if abs(angle_to_goal - theta) > 0.12:
        turtle_vel.linear.x = 0.0
        turtle_vel.angular.z = 0.3 * (t1-t0)
        print(angle_to_goal - theta)
    else:
        turtle_vel.linear.x = 0.5*(t1-t0)
        turtle_vel.angular.z = 0.0

    pub.publish(turtle_vel)
    r.sleep()    
