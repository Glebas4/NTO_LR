1.-----------------------------------------------
nano genmap .py
cd catkin_ws/src/sitl_gazebo/models
git clone nttp://github.com/bart02/dronepoint.git

mv dronepoint/dronepoint_blue .
mv dronepoint/dronepoint_red .
mv dronepoint/dronepoint_green .
mv dronepoint/dronepoint_yellow .

rm -rf dronepoint/
--------------------------------------------------
