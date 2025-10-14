import xml.etree.ElementTree as ET
import random


class cube:
    def __init__(self, x, y, color):
        self.x = x
        self.y = y
        self.color = color
        self.path = "dronepoint/dronepoint_" + color + "/dronepoint_" + color + ".sdf"

    def file_write(self):
        tree = ET.parse(self.path)
        root = tree.getroot()
        val = self.x + " " + self.y + " "+ "0 0 0 0"
        ET.set('pose', val)
        tree.write(self.path)


def main():
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
    
    dronepoint_blue = cube(x_list[0], y_list[0], "blue")
    dronepoint_green = cube(x_list[1], y_list[1], "green")
    dronepoint_yellow = cube(x_list[2], y_list[2], "yellow")
    dronepoint_red = cube(x_list[3], y_list[3], "red")


if __name__ == '__main__':
    main()
        
