import rospy
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2 as cv
import math


bridge = CvBridge()
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
pub = rospy.Publisher('buildings', String, queue_size=1)
colors = {
    "red"   : ((0, 0, 220),(50, 50, 220)),
    "green" : ((0, 220, 0),(50, 255, 50)),
    "blue"  : ((255, 0, 0),(255, 60, 60)),
    "yellow": ((0, 220, 220),(0, 255, 255)) 
}
buildings = []


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)


#def clear_map():
#   

def scan():
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
    for col, val in colors.items():
        bin = cv.inRange(img, val[0], val[1])
        count = cv.countNonZero(bin)
        if count > 30:
            return col
        
    return False


def flight(x, y):
    navigate_wait(x=x, y=y, z=2)
    result = scan()
    if result:
        buildings.append((result, str(x), str(y)))
    #pub.publish(data=buildings)
    print(buildings)

def main():
    navigate_wait(x=0, y=0, z=2, frame_id="body", auto_arm=True)
    y = 0
    while y != 9:
        if not round(y) % 2:
            x = 0.0
            while x != 10.0:
                flight(x, y)
                rospy.sleep(1)
                x += 0.5
            y += 0.5
        else:
            x = 10.0
            while x != 10.0:
                flight(x, y)
                rospy.sleep(1)
                x -= 0.5
            y += 0.5
        

    navigate_wait(x=0, y=0, z=2, frame_id="aruco_map")
    land()
    print("done")


if __name__ == '__main__':
    rospy.init_node('flight')
    main()
