import rospy
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
#from std_msgs.msg import StringArray
import cv2 as cv
import math
import numpy as np


bridge = CvBridge()
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
#pub = rospy.Publisher('buildings', StringArray, queue_size=1)

low_red = ((0, 240, 240), (15, 255, 255))
up_red = ((350, 240, 240),(360, 255, 255))

colors = {
    "red"   : cv.bitwise_or(((350,250,250),(360, 255, 255)), ((0,250,250),(15, 255, 255))),
    "green" : ((50, 240, 240),(90, 255, 255)),
    "blue"  : ((160, 240, 240),(170, 255, 255)),
    "yellow": ((30, 255, 255),(45, 255, 255)) 
}
buildings = []


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


def scan():
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8') [100:140,140:180]
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    for col, val in colors.items():
        bin = cv.inRange(hsv, val[0], val[1])
        count = cv.countNonZero(bin)
        if count > 10:
            return col
        
    return False


def flight(x, y):
    navigate_wait(x=x, y=y, z=2)
    rospy.sleep(2)
    result = scan()
    if result:
        buildings.append((result, str(x), str(y)))
        #pub.publish(data=buildings)
        print(*buildings)


def main():
    navigate_wait(x=0, y=0, z=2, frame_id="body", auto_arm=True)
    for y in range(9):
        if not y % 2:
            for x in range(9):
                flight(x, y)
        else:
            for x in range(9, -1, -1):
                flight(x, y)
        

    navigate_wait(x=0, y=0, z=2, frame_id="aruco_map")
    land()
    print("done")


if __name__ == '__main__':
    rospy.init_node('flight')
    main()
