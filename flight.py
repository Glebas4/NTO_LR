import rospy
from clover import srv
from std_srvs.srv import Trigger
from cv_bridge import CvBridge
from sensor_msgs.msg import Image
from std_msgs.msg import String
import cv2 as cv
import math

rospy.init_node('flight')

bridge = CvBridge()
get_telemetry = rospy.ServiceProxy('get_telemetry', srv.GetTelemetry)
navigate = rospy.ServiceProxy('navigate', srv.Navigate)
land = rospy.ServiceProxy('land', Trigger)
pub = rospy.Publisher('buildings', String, queue_size=1)
colors = {
    "red"   : ((0, 200, 0),(10, 255, 10)),
    "green" : ((100, 100, 100),(150, 150, 150)),
    "blue"  : ((50, 50, 50),(80, 80, 80)),
    "yellow": ((30, 30, 30),(70, 70, 70)) 
}
buildings = []


def navigate_wait(x=0, y=0, z=0, yaw=float('nan'), speed=0.5, frame_id='aruco_map', auto_arm=False, tolerance=0.2):
    navigate(x=x, y=y, z=z, yaw=yaw, speed=speed, frame_id=frame_id, auto_arm=auto_arm)

    while not rospy.is_shutdown():
        telem = get_telemetry(frame_id='navigate_target')
        if math.sqrt(telem.x ** 2 + telem.y ** 2 + telem.z ** 2) < tolerance:
            break
        rospy.sleep(0.2)
        return True


def scan():
    img = bridge.imgmsg_to_cv2(rospy.wait_for_message('main_camera/image_raw', Image), 'bgr8')
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    for col, val in colors.items():
        bin = cv.inRange(hsv, val[0], val[1])
        count = cv.countNonZero(bin)
        if count>30:
            return col
        
    return False


def main():
    navigate_wait(x=0, y=0, z=2, frame_id="body", auto_arm=True)
    for y in range(10):
        if not y % 2:
            for x in range(10):
                print(x,y)
                resp = navigate_wait(x=x, y=y, z=2)
                while not resp:
                    pass
                result = scan()
                if result:
                    buildings.append((result, str(x), str(y)))
                pub.publish(data=buildings)
        else:
            for x in range(10, 0, -1):
                print(x,y)
                resp = navigate_wait(x=x, y=y, z=2)
                while not resp:
                    pass
                result = scan()
                if result:
                    buildings.append((result, str(x), str(y)))
                pub.publish(data=buildings)
        

    navigate_wait(x=0, y=0, z=2, frame_id="aruco_map")
    land()
    print("done")


if __name__ == '__main__':
    main()
