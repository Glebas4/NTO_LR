#!/bin/bash

echo "Setup started"

rm /home/catkin_ws/src/clover/clover/launch/aruco.launch
rm /home/catkin_ws/src/clover/clover/launch/clover.launch

cd /home/clover/NTO_LR/dronepoint/dronepoints
mv dronepoint_red dronepoint_green dronepoint_blue dronepoint_yellow /home/clover/catkin_ws/src/sitl_gazebo/models
if [ $? -eq 0 ]; then
    echo "Models have been successfully moved to home/clover/catkin_ws/src/sitl_gazebo/models"
else
    echo "ERROR: $?"
fi

cd /home/clover/NTO_LR/launch
mv aruco.launch clover.launch /home/clover/catkin_ws/src/clover/clover/launch
if [ $? -eq 0 ]; then
    echo "Launch files have been successfully configured"
else
    echo "ERROR: $?"
fi

cd /home/clover/NTO_LR
rm -rf dronepoint
rm -rf launch

echo "Done"
