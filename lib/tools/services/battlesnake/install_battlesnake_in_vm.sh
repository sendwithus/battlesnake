#!/bin/bash
: <<__

This installs battlesnake into the VM
  it does the following:
    * copies the project from /vagrant (a mount at the project directory of the host system) into a ./battlesnake dir
    * installs prerequisites
    * creates a logs directory

__


mkdir battlesnake
cp -r /vagrant/.  battlesnake

cd battlesnake

CFLAGS='-std=c99' pip install -r requirements.txt

sudo apt-get install -y python-pip
sudo apt-get install -y git
sudo pip install pymongo

# install nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
nvm install
nvm use

sudo gem install foreman

# create the log file for battlesnake
mkdir logs
