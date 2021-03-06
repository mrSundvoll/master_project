# Master project
This repository contains all the code for my master project, conducted the spring 2020. The '/catkin_ws' folder contains the developed system and is the only relevant folder. The '/investiagation' folder contains investigations and various other code that was made along the way and is kept for personal reference.

## Installation
Prerequisites:
* Ubuntu Kinetic (16.04)

### Install ROS Kinetic
Follow this guide: http://wiki.ros.org/kinetic/Installation/Ubuntu

### Install Gazebo 7.0
sudo apt-get install ros-kinetic-gazebo-ros

### ROS packages
* uuv_simulator (https://github.com/uuvsimulator/uuv_simulator)
sudo apt install ros-kinetic-uuv-simulator

* ardrone_autonomy (https://ardrone-autonomy.readthedocs.io/en/latest/installation.html)
```
sudo apt-get install ros-kinetic-ardrone-autonomy
```

* tum_simulator on Kinetic and Gazebo 7 (https://github.com/eborghi10/AR.Drone-ROS)
    (Download files and place them in folder /ardrone_simulator_gazebo7)

### Python packages
* Numpy 1.16.6
* Scipy 1.2.2
* Matplotlib 2.2.4
* OpenCV 3.3.1-dev

Can be install using pip:
```
sudo apt-get install python-pip
python -m pip install --user numpy==1.16.6 scipy==1.2.2 matplotlib==2.2.4
```
and apt-get:
```
sudo apt-get install python-opencv
```

### Add the necessary models
Add models to the hidden folder .gazebo/models
* Landing platform (helipad)
* ReVolt (revolt)

### Other useful things:
* Terminator, for multiple pages in one window
```
sudo apt-get install terminator
```

### DDPG package
The DDPG package made by Daniel Tavakoli is added in a separate package.

### To run the DDPG model:
* Tensorflow 1.15.0
* Keras 2.2.4
* tqdm 4.46.0

```
pip install tensorflow==1.15.0
pip install Keras==2.2.4
pip install tqdm==4.46.0
```

## Running the system

### Connect to physical quadcopter
Turn the quadcopter on and connect to it over WiFI. Then run
```
roslaunch uav_vision real_ar2.launch
```
and switch to bottom camera
```
rosservice call /ardrone/setcamchannel 1
```

### Start simulator and connect to simulated quadcopter
Run
```
roslaunch uav_vision sim_ar2.launch
```

### View the output from the quadcopters bottom camera
Run
```
roslaunch uav_vision camera_view.launch
```

### Start the position estimator
Run
```
roslaunch uav_vision perception_system.launch
```

### Joystick:
* Connect the PS4 controller to the computer via Bluetooth. Then run
```
roslaunch uav_vision joystick.launch
```

### Start the PID controller
Run
```
rosrun uav_vision pid_controller.py
```

### Start the Automated Landing Planner
Run
```
rosrun uav_vision automated_landing.py
```

### To land with DDPG
Run
```
rosrun ddpg ddpg_hover_descend.py
```