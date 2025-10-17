#!/bin/bash

echo "Setup started"
cd dronepoint/dronepoints
mv dronepoint_red dronepoint_green dronepoint_blue dronepoint_yellow /home/clover/catkin_ws/src/sitl_gazebo/models

if [ $? -eq 0 ]; then
    echo "Models have been successfully moved to home/clover/catkin_ws/src/sitl_gazebo/models"
else
    echo "ERROR: $?"
fi
echo "Done"
