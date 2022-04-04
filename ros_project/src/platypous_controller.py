#!/usr/bin/env python3
import rospy
import time
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

class PlatypousMain:
    def __init__(self):
        rospy.init_node('platypous_controller', anonymous=True)
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.cb_scan_cp)
    
    # Callback function to receive scan datas
    def cb_scan_cp(self, msg):
        self.scan_cp = msg

    def scan(self, degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp
        
        #for x in range(len(p.ranges)):
        #    Distance.Array.append(p.ranges[x])
        #    if p.ranges[x] == min(p.ranges):
        #        print("index: " + str(x) + " min value: " + str(min(p.ranges)))
        
        scan_front = 692-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front.append(p.ranges[x+scan_front])
        
        scan_front_l = 70-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front_Left.append(p.ranges[x+scan_front_l])

        scan_front_r = 616-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front_Right.append(p.ranges[x+scan_front_r])

        scan_back = 355-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Back.append(p.ranges[x+scan_back])
        
        scan_left = 174-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Left.append(p.ranges[x+scan_left])
        
        scan_right = 523-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Right.append(p.ranges[x+scan_right])
        
        Distance.f_avg = PlatypousMain.Average(Distance.Front)
        Distance.f_l_avg = PlatypousMain.Average(Distance.Front_Left)
        Distance.f_r_avg = PlatypousMain.Average(Distance.Front_Right)
        Distance.b_avg = PlatypousMain.Average(Distance.Back)
        Distance.l_avg = PlatypousMain.Average(Distance.Left)
        Distance.r_avg = PlatypousMain.Average(Distance.Right)

        #print(type(Distance.f_avg))

        if(type(Distance.f_avg) != float):
            Distance.f_avg = 100
        elif(type(Distance.f_l_avg) != float):
            Distance.f_l_avg = 100
        elif(type(Distance.f_r_avg) != float):
            Distance.f_r_avg = 100
        elif(type(Distance.b_avg) != float):
            Distance.b_avg = 100
        elif(type(Distance.l_avg) != float):
            Distance.l_avg = 100
        elif(type(Distance.r_avg) != float):
            Distance.r_avg = 100

        #print("Front: " + str(Distance.Front))

        print("Front avg: " + str(round(Distance.f_avg, 4)))
        print("Front Left avg: " + str(round(Distance.f_l_avg, 4)))
        print("Front Right avg: " + str(round(Distance.f_r_avg, 4)))
        #print("Left: " + str(round(Distance.l_avg, 4)))
        #print("Right: " + str(round(Distance.r_avg, 4)))
        #print("Back: " + str(round(Distance.b_avg, 4)))
        print()
        
        Distance.Front.clear()
        Distance.Front_Left.clear()
        Distance.Front_Right.clear()
        Distance.Back.clear()
        Distance.Left.clear()
        Distance.Right.clear()

        PlatypousController.go(self, x_speed, z_angular)

    def Average(array):
        return sum(array) / len(array)

class Distance():
    Array = []
    Front = []
    f_avg = 3
    Front_Left = []
    f_l_avg = 3
    Front_Right = []
    f_r_avg = 3

    Right = []
    r_avg = 3
    Left = []
    l_avg = 3
    Back = []
    b_avg = 3


class PlatypousController:    
    def go(self, x_speed, z_angular):
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        vel_msg = Twist()

        if((Distance.f_avg > 2.5) and (Distance.f_l_avg > 2.5) and (Distance.f_r_avg > 2.5)):
            vel_msg.linear.x = abs(x_speed)
            self.twist_pub.publish(vel_msg)
            print("Elso if")

        else:
            print("Belépett")
            if Distance.l_avg >= Distance.r_avg and Distance.f_avg < 1.2:
                print("1")
                vel_msg.linear.x = -abs(x_speed)
                vel_msg.angular.z = z_angular
                self.twist_pub.publish(vel_msg)
            elif Distance.l_avg < Distance.r_avg and Distance.f_avg < 1.2:
                print("2")
                vel_msg.linear.x = -abs(x_speed)
                vel_msg.angular.z = -z_angular
                self.twist_pub.publish(vel_msg)
            elif Distance.f_l_avg <= Distance.f_r_avg:
                print("3")
                x_speed = x_speed/2
                vel_msg.linear.x = abs(x_speed)
                vel_msg.angular.z = -z_angular
                self.twist_pub.publish(vel_msg)
                #print("Masodik if")

            elif Distance.f_r_avg > Distance.f_r_avg:
                print("4")
                x_speed = x_speed/2
                vel_msg.linear.x = abs(x_speed)
                vel_msg.angular.z = z_angular
                self.twist_pub.publish(vel_msg)
                #print("Harmadik if")

if __name__ == '__main__':
    pm = PlatypousMain()

    #pm.scan(17, 0.3, 0.5)

    # 1. Front scan view degree
    # 2. Speed
    # 3. Rotation
    while not rospy.is_shutdown():
        pm.scan(17, 0.5, 0.2)


    #rosrun ros_project platypous_controller.py
