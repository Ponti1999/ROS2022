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

    def scan(self, front_degree, front_side_degree, side_degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp

        scan_front_f = 719 - front_side_degree
        for x in range(front_side_degree):
            Distance.Front_Focus.append(round(p.ranges[x+scan_front_f], 4))
        
        for x in range(front_side_degree):
            Distance.Front_Focus.append(round(p.ranges[x], 4))

        # print("Front Focus Min: " + str(min(Distance.Front_Focus)))
        # print("Front Focus: " + str(Distance.Front_Focus))
        # print()
                
        scan_front = 719-front_degree
        for x in range(front_degree):
            if p.ranges[x+scan_front] > p.range_min and p.ranges[x+scan_front] < p.range_max:
                Distance.Front.append(round(p.ranges[x+scan_front], 4))

        for x in range(front_degree):
            if p.ranges[x] > p.range_min and p.ranges[x] < p.range_max:
                Distance.Front.append(round(p.ranges[x], 4))

        # print("Front Min: " + str(round(min(Distance.Front), 4)))
        # print("Front: " + str(Distance.Front))
        # print()
        

        scan_front_l = front_degree
        for x in range(front_side_degree*2):
            if p.ranges[x+scan_front_l] > p.range_min and p.ranges[x+scan_front_l] < p.range_max:
                Distance.Front_Left.append(round(p.ranges[x+scan_front_l], 4))

        # print("Front Left Min: " + str(min(Distance.Front_Left)))
        # print("Front Left: " + str(Distance.Front_Left))
        # print()


        scan_front_r = scan_front - (front_side_degree *2)
        for x in range(front_side_degree*2):
            if p.ranges[x+scan_front_r] > p.range_min and p.ranges[x+scan_front_r] < p.range_max:
                Distance.Front_Right.append(round(p.ranges[x+scan_front_r], 4))

        # print("Front Right Min: " + str(min(Distance.Front_Right)))
        # print("Front Right: " + str(Distance.Front_Right))

        
        scan_left = scan_front_l
        for x in range(side_degree*2):
            Distance.Left.append(p.ranges[x+scan_left])
        
        scan_right = scan_front_r - (side_degree*2)
        for x in range(side_degree*2):
            Distance.Right.append(p.ranges[x+scan_right])

        scan_back = 360 - (front_degree * 2)
        for x in range(front_degree*2):
            if p.ranges[x+scan_back] > p.range_min and p.ranges[x+scan_back] < p.range_max:
                Distance.Back.append(p.ranges[x+scan_back])
        
        scan_back_r = scan_back + (front_degree * 2)
        for x in range(front_side_degree*2):
            if p.ranges[x+scan_back_r] > p.range_min and p.ranges[x+scan_back_r] < p.range_max:
                Distance.Back_Right.append(p.ranges[x+scan_back_r])

        scan_back_l = scan_back - (front_side_degree * 2)
        for x in range(front_side_degree*2):
            if p.ranges[x+scan_back_l] > p.range_min and p.ranges[x+scan_back_l] < p.range_max:
                Distance.Back_Left.append(p.ranges[x+scan_back_l])


        PlatypousController.go(self, x_speed, z_angular)

    def clear():
        Distance.Front.clear()
        Distance.Front_Left.clear()
        Distance.Front_Right.clear()
        Distance.Back.clear()
        Distance.Left.clear()
        Distance.Right.clear()

class Distance():
    Front_Focus = []
    Front = []
    Front_Left = []
    Left = []
    Back_Right = []
    Back = []
    Back_Left = []
    Right = []
    Front_Right = []


class PlatypousController:
    def go(self, x_speed, z_angular):
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        vel_msg = Twist()

        #pozitív angukar_z esetén balra fordul

        print("Front min: " + str(min(Distance.Front)))
        print("Front right min: " + str(min(Distance.Front_Right)))
        print("Front left min: " + str(min(Distance.Front_Left)))
        print("Back right min: " + str(min(Distance.Back_Right)))
        print("Back left min: " + str(min(Distance.Back_Left)))
        print()
        if min(Distance.Front) < 1.1:

            if (min(Distance.Front_Right) < 1) or (min(Distance.Front_Left) > (min(Distance.Front_Right) + 0.8)):
                if min(Distance.Front) > 1 and min(Distance.Front_Left) > (min(Distance.Front_Right) + 0.8):
                    print("Bal")
                    vel_msg.linear.x = x_speed/2
                    vel_msg.angular.z = z_angular
                    self.twist_pub.publish(vel_msg)
                elif min(Distance.Front) > 0.5:
                    if min(Distance.Front_Left) > 1:
                        print("1")
                        vel_msg.linear.x = x_speed/2
                        vel_msg.angular.z = z_angular
                        self.twist_pub.publish(vel_msg)
                    elif min(Distance.Back_Right) > 1:
                        print("2")
                        vel_msg.linear.x = -x_speed*0.5
                        vel_msg.angular.z = -z_angular
                        self.twist_pub.publish(vel_msg)
                elif min(Distance.Back) > 0.5 or min(Distance.Back_Left) > 0.5 or min(Distance.Back_Right) > 0.5:
                    if min(Distance.Back) > 0.5:
                        print("3")
                        vel_msg.angular.z = 0
                        vel_msg.linear.x = -x_speed*0.4
                        self.twist_pub.publish(vel_msg)
                    elif min(Distance.Back_Right) > 0.5:
                        print("4")
                        vel_msg.linear.x = -x_speed*0.4
                        vel_msg.angular.z = -z_angular
                        self.twist_pub.publish(vel_msg)
                    elif min(Distance.Back_Left) > 0.5:
                        print("5")
                        vel_msg.linear.x = -x_speed*0.4
                        vel_msg.angular.z = z_angular
                        self.twist_pub.publish(vel_msg)
            elif (min(Distance.Front_Left) < 1) or (min(Distance.Front_Right) > (min(Distance.Front_Left) + 0.8)):
                if min(Distance.Front) > 1 and min(Distance.Front_Right) > (min(Distance.Front_Left) + 0.8):
                    print("Bal")
                    vel_msg.linear.x = x_speed/2
                    vel_msg.angular.z = z_angular
                    self.twist_pub.publish(vel_msg)
                elif min(Distance.Front) > 0.5:
                    if min(Distance.Front_Right) > 1:
                        print("3")
                        vel_msg.linear.x = x_speed/2
                        vel_msg.angular.z = -z_angular
                        self.twist_pub.publish(vel_msg)
                    elif(min(Distance.Back_Left) > 1):
                        print("7")
                        vel_msg.linear.x = -x_speed*0.5
                        vel_msg.angular.z = z_angular
                        self.twist_pub.publish(vel_msg)
                elif min(Distance.Back) > 0.5 or min(Distance.Back_Left) > 0.5 or min(Distance.Back_Right) > 0.5:
                    if min(Distance.Back) > 0.5:
                        print("8")
                        vel_msg.angular.z = 0
                        vel_msg.linear.x = -x_speed*0.4
                        self.twist_pub.publish(vel_msg)
                    elif min(Distance.Back_Right) > 0.5:
                        print("9")
                        vel_msg.linear.x = -x_speed*0.4
                        vel_msg.angular.z = -z_angular
                        self.twist_pub.publish(vel_msg)
                    elif min(Distance.Back_Left) > 0.5:
                        print("10")
                        vel_msg.linear.x = -x_speed*0.4
                        vel_msg.angular.z = z_angular
                        self.twist_pub.publish(vel_msg)
            #Ide egy hátrafelé fordulásos implementálás
            
            else:
                print("nice")
        else:
            vel_msg.linear.x = x_speed
            self.twist_pub.publish(vel_msg)

        #vel_msg.linear.x = x_speed/2
        #vel_msg.angular.z = z_angular
        #self.twist_pub.publish(vel_msg)


        PlatypousMain.clear()

if __name__ == '__main__':
    pm = PlatypousMain()

    # pm.scan(80, 10, 40, 0.5, 0.4)

    #front_degree, front_side_degree, side_degree, x_speed, z_angular
    # 1. Front scan view degree
    # 2. Speed
    # 3. Rotation
    while not rospy.is_shutdown():
       pm.scan(75, 15, 40, 0.6, 0.45)


    #cd Documents/PlatypOUs-Mobile-Robot-Platform/
    #./platypous start_sim
    #source ~/catkin_ws/devel/setup.bash
    #clear
    #rosrun ros_project platypous_controller.py
