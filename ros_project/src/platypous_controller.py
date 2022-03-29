import rospy
import math
import time
import numpy as np
from enum import Enum 
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class Directions():
    Front = []
    f_avg = 0.5
    Right = []
    r_avg = 1
    Left = []
    l_avg = 1
    Back = []
    b_avg = 1

class Helper:
    def Average(array):
            return sum(array) / len(array)

class PlatypousController:
    def __init__(self):
        rospy.init_node('platypous_controller', anonymous=True)
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.cb_scan_cp)
    
    
    # Callback function to receive scan datas
    def cb_scan_cp(self, msg):
        self.scan_cp = msg
        #print("A cb-ben mukodik: " + str(self.scan_cp.angle_min))
        #print()

    def side_arrays(self, degree):
        time.sleep(0.4)
        p = self.scan_cp

        scan_front = 675
        a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Directions.Front.append(p.ranges[x+scan_front])

        #rospy.loginfo(p.ranges)        
            
        Directions.f_avg = Helper.Average(Directions.Front)
        #print("Atlag: " + str(Directions.f_avg))

        if Directions.f_avg != "inf":
            print("Szög: " + str(degree) + "°" + str(Directions.Front))
            for i in range(len(p.ranges)):
                if p.ranges[i] == min(p.ranges):
                    print("index: " + str(i) + " min value: " + str(min(p.ranges)))
        
        Directions.Front.clear()
        
    def go_straight(self, forward, speed, degree):
        vel_msg = Twist()
        if forward:
            vel_msg.linear.x = speed
            #vel_msg.angular.z = 0.7
        else:
            vel_msg.linear.x = -speed
            #vel_msg.angular.z = -0.7        
        
        rate = rospy.Rate(100) # Hz
        self.twist_pub.publish(vel_msg)
        while(Directions.f_avg > 0.3):
            PlatypousController().side_arrays(degree)
            if Directions.f_avg < 2.5:
                vel_msg.linear.x = vel_msg.linear.x/1.1
                print("Speed: " + str(vel_msg.linear.x))
            print("Atlag: " + str(Directions.f_avg))
            self.twist_pub.publish(vel_msg)
            rate.sleep()    # loop rate

if __name__ == '__main__':
    pc = PlatypousController()
    
    while(True):
        if Directions.f_avg > 0.3:
            forward = True
        else:
            print("DONE")
            exit()

        pc.go_straight(forward, 0.5, 17)
        #forward = not forward