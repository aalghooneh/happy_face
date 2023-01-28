import rclpy
from rclpy.node import Node
from turtlesim.msg import Pose
from geometry_msgs.msg import Twist
from math import sqrt,atan2
class closedLoopController(Node):
    def __init__(self, publisher_msg, publishing_topic, qos_publisher,
            subscriber_msg, subscribing_topic, qos_subscription, publishing_cycle):
        super().__init__("closedLoopController")
        self.publisher=self.create_publisher(publisher_msg, publishing_topic, qos_profile=qos_publisher)
        self.create_subscription(subscriber_msg, subscribing_topic, self.subscriberCallback, qos_profile=qos_subscription)
        self.create_timer(publishing_cycle, self.timerCallback)
        x=8.0
        y=8.0
        theta=0.0
        self.goal=[x,y,theta]
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
                self.publisher.publish(vel_msg)
            else:
                vel_msg=Twist()
                self.publisher.publish(vel_msg)
                raise SystemExit
    def subscriberCallback(self,poseMsg):
        x=poseMsg.x
        y=poseMsg.y
        theta=poseMsg.theta
        self.pose=[x,y,theta]
    def calculate_linear_error(self):
        kp_x=0.1
        threshold=0.1
        error=sqrt( (self.pose[0]-self.goal[0])**2 + (self.pose[1]-self.goal[1])**2)
        self.reached_goal=True if error <threshold else False
        return kp_x * error
    def calculate_angular_error(self):
        theta_goal=atan2(self.goal[1]-self.pose[1], self.goal[0]-self.pose[0])
        theta_now=self.pose[2]
        kp_theta=0.5
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
