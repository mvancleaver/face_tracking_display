# General Clean-Up and Dependancies
sudo rm -r ~/Documents ~/Music ~/Pictures ~/Public ~/Templates ~/Videos ~/examples.desktop
sudo apt update && sudo apt install -y build-essential byobu i2c-tools git arp-scan nano git

# Python 2
sudo apt install -y python python-pip python3 pyton3-pip
pip install -y opencv-python future dlib smbus
pip install -y --upgrade imutils

# Python 3 + Circuit Python
sudo apt install -y python3 pyton3-pip
pip3 install -y opencv-python future dlib smbus
sudo pip3 install adafruit-circuitpython-servokit adafruit-circuitpython-bno055
pip3 install -y --upgrade imutils
sudo apt update
sudo apt upgrade
sudo pip3 install --upgrade setuptools
pip3 freeze - local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
sudo groupadd -f -r gpio
sudo usermod -a -G gpio user
cd ~
git clone https://github.com/NVIDIA/jetson-gpio.git
sudo cp ~/jetson-gpio/lib/python/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d

# javascipt / node


# Jetson Package Setups
mkdir JetsonHacksSetup/ && cd JetsonHacksSetup/
# Install Librealsense
git clone https://github.com/JetsonHacksNano/installLibrealsense.git
cd installLibrealsense
./installLibrealsense.sh
cd ..
git clone https://github.com/JetsonHacksNano/installVSCode.git
cd installVSCode
./installVSCode.sh
cd 

mkdir exapmpleRepos && cd exapmpleRepos
git clone https://github.com/antoinelame/GazeTracking.git
pip install -r requirements.txt
#git clone https://github.com/1adrianb/face-alignment.git
pip3 install face-alignment	
cd ..
