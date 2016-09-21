pip install -U platformio
printf "Host *\n\tStrictHostKeyChecking no" > ~/.ssh/config
sudo mkdir /Robot
sudo chmod 0777 /Robot
sudo mkdir /Robot/ArduinoLibraries
sudo chmod 0777 /Robot/ArduinoLibraries
git clone https://github.com/utk-robotics-2017/ArduinoLibraries.git /Robot/ArduinoLibraries
current_directory=$(pwd)
cd /Robot/ArduinoLibraries
sed -i.bak 's/git@github.com:/https:\/\/github.com\//g' .gitmodules
git submodule sync
git submodule update --init
cd $current_directory
