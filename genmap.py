import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point
import random
import sys
import math

spawn_service = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
delete_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
dronepoints = ["blue", "green", "yellow", "red"]

class building:
    def __init__(self, x, y, color, name):
        self.x = x
        self.y = y
        self.z = 0

        self.pose = Pose()
        self.pose.position = Point(self.x, self.y, self.z)

        self.name = name
        self.color = color
        self.path = "/home/clover/catkin_ws/src/sitl_gazebo/models/dronepoint_" + color + "/dronepoint_" + color + ".sdf"

    def spawn(self):
        with open(self.path, 'r') as f:
            sdf_file = f.read()

        gen = spawn_service(model_name=self.name,
                             model_xml=sdf_file,
                             robot_namespace='',
                             initial_pose=self.pose,
                             reference_frame="world")
        print(gen.status_message, self.name, self.color, "building")

    def delete(self):
        resp = delete_service(self.name)
        print(resp.status_message, self.name, self.color)


def gen_points():
    global points
    points = []
    while len(points) < 5:
        x = round(random.uniform(0, 9), 1)
        y = round(random.uniform(0, 9), 1)
        if all(math.sqrt((point[0] - x)**2 + (point[1] - y)**2) >=1 for point in points):
            points.append((x, y))

    return points

        


def main():
    if len(sys.argv)>1:
        dronepoint_blue   = building(0, 0, "building", "1st")
        dronepoint_green  = building(0, 0, "building", "2nd")
        dronepoint_yellow = building(0, 0, "building", "3rd")
        dronepoint_red    = building(0, 0, "building", "4th")
        dronepoint_random = building(0, 0, "building", "5th")

        dronepoint_blue.delete()
        dronepoint_green.delete()
        dronepoint_yellow.delete()
        dronepoint_red.delete()
        dronepoint_random.delete()


    else:
        cords = gen_points()
    
        dronepoint_blue   = building(points[0][0], points[0][1], random.choice(dronepoints), "1st")
        dronepoint_green  = building(points[1][0], points[1][1], random.choice(dronepoints), "2nd")
        dronepoint_yellow = building(points[2][0], points[2][1], random.choice(dronepoints), "3rd")
        dronepoint_red    = building(points[3][0], points[3][1], random.choice(dronepoints), "4th")
        dronepoint_random = building(points[4][0], points[4][1], random.choice(dronepoints), "5th")


        dronepoint_blue.spawn()
        dronepoint_green.spawn()
        dronepoint_yellow.spawn()
        dronepoint_red.spawn()
        dronepoint_random.spawn()


if __name__ == '__main__':
    rospy.init_node("kubiki")
    main()
