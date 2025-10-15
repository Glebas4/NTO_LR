import rospy
from gazebo_msgs.srv import SpawnModel, DeleteModel
from geometry_msgs.msg import Pose, Point
import random
import sys

spawn_service = rospy.ServiceProxy('/gazebo/spawn_sdf_model', SpawnModel)
delete_service = rospy.ServiceProxy('/gazebo/delete_model', DeleteModel)
dronepoints = ["blue", "green", "yellow", "red"]

class building:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.z = 0

        self.pose = Pose()
        self.pose.position = Point(self.x, self.y, self.z)
        #self.q = Quaternion(x=0, y=0, z=0, w=1)
        #self.pose.orientation = Quaternion(self.q)

        self.color = color
        self.path = "catkin_ws/src/sitl_gazebo/models/dronepoint_" + color + "/dronepoint_" + color + ".sdf"

    def spawn(self):
        with open(self.path, 'r') as f:
            sdf_file = f.read()

        gen = spawn_service(model_name=self.color,
                             model_xml=sdf_file,
                             robot_namespace='',
                             initial_pose=self.pose,
                             reference_frame="world")
        print(gen.status_message, self.color , "building")

    def delete(self):
        resp = delete_service(self.color)
        print(resp.status_message, self.color , "building")
     


def main():
    if len(sys.argv)>1:
        dronepoint_blue = building(0, 0, "blue")
        dronepoint_green = building(0, 0, "green")
        dronepoint_yellow = building(0, 0, "yellow")
        dronepoint_red = building(0, 0, "red")

        dronepoint_blue.delete()
        dronepoint_green.delete()
        dronepoint_yellow.delete()
        dronepoint_red.delete()


    else:
        x_list = []
        y_list = []
        free_x = [0,1,2,3,4,5,6,7,8,9]
        free_y = [0,1,2,3,4,5,6,7,8,9]

        for x in range(4):
            x = random.choice(free_x)
            x_list.append(x)
            free_x.remove(x)
        for y in range(4):
            y = random.choice(free_y)
            y_list.append(y)
            free_y.remove(y)
    
        dronepoint_blue = building(x_list[0], y_list[0], "blue")
        dronepoint_green = building(x_list[1], y_list[1], "green")
        dronepoint_yellow = building(x_list[2], y_list[2], "yellow")
        dronepoint_red = building(x_list[3], y_list[3], "red")

        dronepoint_blue.spawn()
        dronepoint_green.spawn()
        dronepoint_yellow.spawn()
        dronepoint_red.spawn()


if __name__ == '__main__':
    rospy.init_node("kubiki")
    main()
