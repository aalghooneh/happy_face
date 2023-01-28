import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import sqrt,atan2
class closedLoopController(Node):
    def __init__(self, publisher_msg, publishing_topic, qos_publisher,
            subscriber_msg, subscribing_topic, qos_subscription, publishing_cycle):
        super().__init__("closedLoopController")
        self.publisher=#create the publisher here
        self.#create the subscriber here to "subscriberCallback" function
        self.#create the timer callback here to "timerCallback" function
        x=8.0# this is your destination in x
        y=8.0# this is your destination in y
        self.goal=[x,y]
        self.reached_goal=False
        self.pose=None
    def timerCallback(self):
        if self.pose is not None:
            vel_msg=Twist()
            if not self.reached_goal:
                vel_msg.linear.x=self.calculate_linear_error()
                vel_msg.linear.y=0.0
                vel_msg.linear.z=0.0
                vel_msg.angular.z=self.calculate_angular_error()
                self.publisher#publish the velocity here
            else:
                vel_msg=Twist()# create empty message
                self.publisher#publish the velocity here
                raise SystemExit
    def subscriberCallback(self,poseMsg):
        x=poseMsg.x
        y=poseMsg.y
        theta=poseMsg.theta
        self.pose=[x,y,theta]
    def calculate_linear_error(self):
        kp_x=# put a gain start with 0.1 to have slow motion
        threshold=#put a threshold for declaring reaching
        error=# calculate the error
        self.reached_goal=True if error <threshold else False
        return kp_x * error
    def calculate_angular_error(self):
        theta_goal=# this is what your theta should be when approaching the goal
        theta_now=# this is what your theta is at every callback
        kp_theta=# this is the controller gain you can start with 0.5
        return kp_theta*(theta_goal-theta_now)


def main(args=None):
    rclpy.init()
    CLC=closedLoopController(Twist, "/turtle1/cmd_vel", 10, Pose, "/turtle1/pose", 10, 0.1)
    try:
        rclpy.spin(CLC)
    except SystemExit:
        print(f"reached there successfully {CLC.pose}")




if __name__=="__main__":
    main()
