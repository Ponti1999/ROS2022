import rospy
import math
from geometry_msgs.msg import Twist

class PlatypousController:
    def __init__(self):
        rospy.init_node('platypous_controller', anonymous=True)
        self.twist_pub = rospy.Publisher('/driver/cmd_vel/nav:', Twist, queue_size=10)


    def go_straight(self, forward):
        vel_msg = Twist()
        if forward:
            vel_msg.linear.x = speed
            vel_msg.linear.y = 1
        else:
            vel_msg.linear.x = -speed
            vel_msg.linear.y = -1
        
        rate = rospy.Rate(100) # Hz
        
        self.twist_pub.publish(vel_msg)
        t0 = rospy.Time.now().to_sec()
        
    while (rospy.Time.now().to_sec() - t0 <= 10)
        self.twist_pub.publish(vel_msg)
        rate.sleep()    # loop rate

if __name__ == '__main__':
    # Init
    pc = PlatypousController()
    forward = True
    
    while(True):
        pc.go_straight(forward)
        forward = not forward

