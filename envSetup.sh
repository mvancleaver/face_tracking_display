# General Clean-Up and Dependancies
sudo rm -r ~/Documents ~/Music ~/Pictures ~/Public ~/Templates ~/Videos ~/examples.desktop
sudo apt update && sudo apt install -y build-essential byobu i2c-tools git arp-scan nano git
echo 'source ~/.bashrc' >> ~/.bash_profile


# Python 3 + Circuit Python
sudo apt install -y python3 python3-pip python3-dev 
pip3 install --upgrade pip
pip3 install future dlib smbus numpy opencv-python
pip3 install adafruit-circuitpython-servokit adafruit-circuitpython-bno055
git clone https://github.com/jrosebr1/imutils.git
cd imutils/
sudo python3 setup.py install
cd 
sudo apt update && sudo apt upgrade
sudo pip3 install --upgrade setuptools
pip3 freeze - local | grep -v '^\-e' | cut -d = -f 1 | xargs -n1 pip3 install -U
sudo groupadd -f -r gpio
sudo usermod -a -G gpio user

git clone https://github.com/NVIDIA/jetson-gpio.git
sudo cp ~/jetson-gpio/lib/python/Jetson/GPIO/99-gpio.rules /etc/udev/rules.d

# Realsense2.0 SDK on Jetson
mkdir lib_src && cd lib_src
sudo apt-get install -y curl libssl-dev libcurl4-openssl-dev libxinerama-dev libxcursor-dev
wget http://www.cmake.org/files/v3.13/cmake-3.13.0.tar.gz
tar xpvf cmake-3.13.0.tar.gz cmake-3.13.0/
cd cmake-3.13.0/
./bootstrap --system-curl
make -j4
echo 'export PATH=/home/nvidia/cmake-3.13.0/bin/:$PATH' >> ~/.bashrc
source ~/.bashrc
cd ..
wget https://github.com/IntelRealSense/librealsense/archive/v2.38.1.tar.gz
tar -xf v2.38.1.tar.gz 
cd librealsense-2.38.1/
./scripts/setup_udev_rules.sh
mkdir build && cd build
cmake ../ -DBUILD_EXAMPLES=true -DBUILD_PYTHON_BINDINGS:bool=true -DBUILD_WITH_CUDA:bool=true -DBUILD_CV_EXAMPLES:bool=true -DCMAKE_CUDA_COMPILER:PATH=/usr/local/cuda/bin/nvcc -DPYTHON_EXECUTABLE=/usr/bin/python3
make && sudo make install
echo 'export PATH=/home/nvidia/cmake-3.13.0/bin/:$PATH' >> ~/.bashrc
echo 'export PATH=/home/nvidia/cmake-3.13.0/bin/:$PATH' >> ~/.bashrc
echo 'export PATH=/home/nvidia/cmake-3.13.0/bin/:$PATH' >> ~/.bashrc
source ~/.bashrc
cd ..
# import pyrealsense2 as rs
# rs.__path__ ['/usr/lib/python3/dist-packages/pyrealsense2']
# sudo cp ~/librealsense/wrappers/python/pyrealsense2/__init__.py /usr/lib/python3/dist-packages/pyrealsense2/
# Jetson Package Setups
mkdir JetsonHacksSetup/ && cd JetsonHacksSetup/
# Jetson VS Code
git clone https://github.com/JetsonHacksNano/installVSCode.git
cd installVSCode
./installVSCode.sh
cd 

mkdir exapmpleRepos && cd exapmpleRepos
git clone https://github.com/antoinelame/GazeTracking.git
pip3 install -r requirements.txt
git clone https://github.com/1adrianb/face-alignment.git
cd ..
