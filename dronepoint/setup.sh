#!/bin/bash

echo "Setup started"
cd dronepoints
mv dronepoint_red dronepoint_green dronepoint_blue dronepoint_yellow /home/clover/catkin_ws/src/sitl_gazebo/models

if [ $? -eq 0 ]; then
    echo "Files have been successfully moved to home/clover/catkin_ws/src/sitl_gazebo/models"
else
    echo "ERROR: $?"
fi

cd ..
mv genmap.py /home/clover

if [ $? -eq 0 ]; then
    echo "genmap.py is ready"
else
    echo "ERROR: $?"
fi

cd
rm -rf dronepoint

if [ $? -eq 0 ]; then
    echo "dronepoint directory has been deleted"
else
    echo "ERROR: $?"
fi

echo "Done"
