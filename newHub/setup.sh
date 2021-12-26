# installs necessary python libraries to run the server
sudo apt-get update
sudo apt-get upgrade

sudo apt-get install python3-pip

sudo python3 -m pip install flask
sudo python3 -m pip install websockets

sudo cp webserver.service /etc/systemd/system/webserver.service
