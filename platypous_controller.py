import rospy
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class PlatypousController:
    def __init__(self):
        rospy.init_node('platypous_controller', anonymous=True)
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.cb_scan)

    # Callback function to receive scan datas
    def cb_scan(self, msg):
        self.scan_array = msg
        #rospy.loginfo(rospy.get_caller_id() + " I heard marker %s", msg)
        p = self.scan_array
        #arr = p.split(',')
        rospy.loginfo(p.ranges)

    def go_straight(self, forward, speed):
        vel_msg = Twist()
        if forward:
            vel_msg.linear.x = speed
            vel_msg.angular.z = 0.7
        else:
            vel_msg.linear.x = -speed
            vel_msg.angular.z = -0.7
        
        rate = rospy.Rate(100) # Hz
        
        self.twist_pub.publish(vel_msg)
        t0 = rospy.Time.now().to_sec()
        
        while (rospy.Time.now().to_sec() - t0 <= 10):
            self.twist_pub.publish(vel_msg)
            rate.sleep()    # loop rate

if __name__ == '__main__':
    pc = PlatypousController()
    forward = True
    
    while(True):
        pc.go_straight(forward, 0.5)
        forward = not forward
        

