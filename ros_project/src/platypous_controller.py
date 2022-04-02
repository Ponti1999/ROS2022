import rospy
import time
import math
from geometry_msgs.msg import Twist
from sensor_msgs.msg import LaserScan

#It is the Main part where the publish and subcribtions happen
# and data collections
#It needs one parameter -> degree which tell the
# front view degree of the lidar scan
#(need to be <= then 28)
class PlatypousMain:
    def __init__(self):
        rospy.init_node('platypous_controller', anonymous=True)
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        rospy.Subscriber("/scan", LaserScan, self.cb_scan_cp)
    
    # Callback function to receive scan datas
    def cb_scan_cp(self, msg):
        self.scan_cp = msg

    def front(self, degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp

        scan_front = 692-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front.append(p.ranges[x+scan_front])
        
        print("Forward: " + str(Distance.f_avg))
        
        pc = PlatypousController()
        pc.go(degree, x_speed, z_angular)

    def back(self, degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp

        scan_back = 355-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front.append(p.ranges[x+scan_back])
        
        print("Backward: " + str(Distance.b_avg))
        
        pc = PlatypousController()
        pc.go(degree, x_speed, z_angular)

    def left(self, degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp

        scan_back = 523-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front.append(p.ranges[x+scan_back])
        
        print("Leftward: " + str(Distance.l_avg))
        print("Degree: " + str(degree) + " speed: " + str(x_speed) + " angular: " + str(z_angular))
        
        pc = PlatypousController()
        pc.rotate(degree, x_speed, z_angular)

    def right(self, degree, x_speed, z_angular):
        time.sleep(0.4)
        p = self.scan_cp

        scan_back = 174-degree
        #a = len(p.ranges)-(degree*2)
        for x in range(degree*2):
            Distance.Front.append(p.ranges[x+scan_back])
        
        print("Rightward: " + str(Distance.r_avg))
        
        pc = PlatypousController()
        pc.rotate(degree, x_speed, z_angular)

        

#Get the LIDAR scan information from Main
#for further calculations
class Distance():
    Front = []
    f_avg = 1
    Right = []
    r_avg = 3
    Left = []
    l_avg = 3
    Back = []
    b_avg = 3


#Variables: x_speed, z_angular
class PlatypousController:
    
    def go(self, degree, x_speed, z_angular):
        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        vel_msg = Twist()
        Distance.f_avg = Helper.Average(Distance.Front)
        if (Distance.f_avg < 2.5):
            print("F: " + str(Distance.f_avg))
            PlatypousController.calculate(self, degree, x_speed, z_angular)
        vel_msg.linear.x = x_speed
        self.twist_pub.publish(vel_msg)
    
    def calculate(self, degree, x_speed, z_angular):
        pm = PlatypousMain()
        pm.left(degree, x_speed, z_angular)
        pm.right(degree, x_speed, z_angular)

    def rotate(self, degree, x_speed, z_angular):
        print("rotate! Degree: " + str(degree) + " speed: " + str(x_speed) + " angular: " + str(z_angular))

        self.twist_pub = rospy.Publisher('/cmd_vel/nav', Twist, queue_size=10)
        vel_msg = Twist()
        #Slow down for turning (for safety)
        slow_down_speed = x_speed / 2
        vel_msg.linear.x = slow_down_speed
        self.twist_pub.publish(vel_msg)

        if(Distance.l_avg <= Distance.r_avg):

            vel_msg.angular.z = -z_angular
            self.twist_pub.publish(vel_msg)
            print("If rotate! Degree: " + str(degree) + " speed: " + str(x_speed) + " angular: " + str(z_angular))
            PlatypousController.go(degree, x_speed, z_angular)
        elif(Distance.l_avg < 2.5 and Distance.r_avg < 2.5):
            PlatypousMain.back(degree, -x_speed, z_angular)
        else:
            print("Else rotate! Degree: " + str(degree) + " speed: " + str(x_speed) + " angular: " + str(z_angular))
            vel_msg.angular.z = z_angular
            self.twist_pub.publish(vel_msg)
            PlatypousController.go(degree, x_speed, z_angular)
            
        PlatypousController.go(degree, x_speed, z_angular)


class Helper:
    def Average(array):
        return sum(array) / len(array)


if __name__ == '__main__':
    pm = PlatypousMain()

    # 1. Front scan view degree
    # 2. Speed
    # 3. Rotation
    while(True):
        pm.front(17, -0.3, 0.5)
    