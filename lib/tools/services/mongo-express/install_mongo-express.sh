#!/bin/bash
: <<__

This installs mongo-express into the VM
  it does the following:
    * installs prerequisites
    * creates a logs directory

__

# install nvm
curl -o- https://raw.githubusercontent.com/creationix/nvm/v0.31.0/install.sh | bash
nvm install 4
nvm use 4

npm install mongo-express

# create the log file for battlesnake
mkdir mongo-express/logs
