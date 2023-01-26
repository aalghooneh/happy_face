import rclpy
from rclpy.node import Node

from geometry_msgs.msg  import Twist
from turtlesim.msg import Pose
from math import pow, atan2, sqrt, floor


class HappyFace(Node):

    def __init__(self):
        super().__init__('happy_face')
        self.publisher_ = self.create_publisher(Twist, '/turtle1/cmd_vel', 10)
        self.subscription = self.create_subscription(Pose, '/turtle1/pose', self.listener_callback, 10)
        self.subscription
        timer_period = 1.0  # seconds
        self.timer = self.create_timer(timer_period, self.timer_callback)
        self.circle_pose = Pose()
        self.goal_pose = [0]*2
        self.init_pose = [0]*2
        self.circle_flag = 1	# Indicator for the timer is in charge of moving the turtle - circling
        self.set_goal = 0	# Indicator for the controller is incharge of mving the turtle - heading to goal pose
        self.skip = 0		# Indicates that we are one iteration far after the circling timer
        # when turtle is still too close to the circle_pose after actually finishing it, the condition (circle_error <= 0.2) will be met. So, we need to skip at least one publishing iteration just after the heading goal starts
        self.goals = 0 # indicates number of goals set
        self.i = 0	# indicates number of publsiher call back
        
    def euclidean_distance(self, goal_pose):
        """Euclidean distance between current pose and the goal."""
        if type(goal_pose) == type (self.goal_pose):
        	return sqrt(pow((goal_pose[0] - self.pose.x), 2) +
		                pow((goal_pose[1] - self.pose.y), 2))
        else:
        	return sqrt(pow((goal_pose.x - self.pose.x), 2) +
		                pow((goal_pose.y - self.pose.y), 2))
		                       
    def timer_callback(self):

        msg =Twist() 
        if self.i == 0:
        	self.circle_pose = self.pose

        if self.circle_flag == 1:
        	msg.linear.x = 0.5
        	msg.linear.y = 0.0
        	msg.angular.z = 0.5

        circle_error = round(self.euclidean_distance(self.circle_pose), 1)
        line_error = self.euclidean_distance(self.goal_pose)
        
        if (( circle_error <= 0.2) and self.skip != self.i) or self.circle_flag == 0:	    
		    
        	self.circle_flag = 0	# Not circling anymore
        	
        	if self.set_goal == 0:		# Set goal pose
        		self.goal_pose = self.init_pose.copy()
        		self.goal_pose[0] = self.goal_pose[0] + 3.0
        		self.goal_pose[1] = self.goal_pose[1] + 3.0
        		self.set_goal = 1
        		self.goals += 1
        		
        	if line_error >= 0.01:       	
        		msg.linear.x = 0.5 * self.euclidean_distance(self.goal_pose)
        		msg.linear.y = 0.0
        		msg.linear.z = 0.0
        		
        		msg.angular.x = 0.0
        		msg.angular.y = 0.0
        		msg.angular.z = 1 * (atan2(self.goal_pose[1] - self.pose.y, self.goal_pose[0] - self.pose.x) - self.pose.theta)
        	        	
        	else:	# Reached goal pose, i.e., euclidean distance <= 0.01
        		print("Adjusting flags")
        		self.circle_flag = 1	# start circling again
        		self.set_goal = 0
        		self.circle_pose = self.pose
        		self.skip = self.i + 1	
        
        if self.goals < 2:       	
        	if self.circle_flag == 1:
        		print("circling")
        	else:
        		print("Heading to goal")
        	self.publisher_.publish(msg)
        	self.i += 1 
        if self.goals==2:
            raise SystemExit
    def listener_callback(self, msg):
        """Callback function which is called when a new message of type Pose is
        received by the subscriber."""
        self.pose = msg
        self.pose.x = round(self.pose.x, 4)
        self.pose.y = round(self.pose.y, 4)
        
        if self.i == 0:
        	self.init_pose[0] = self.pose.x
        	self.init_pose[1] = self.pose.y
def main(args=None):
    rclpy.init(args=args)

    happy_face = HappyFace()
    try:
        rclpy.spin(happy_face)
    except SystemExit:
        print("It's a smiley face right?!")
    # Destroy the node explicitly
    # (optional - otherwise it will be done automatically
    # when the garbage collector destroys the node object)
    happy_face.destroy_node()
    rclpy.shutdown()


if __name__ == '__main__':
    main()

