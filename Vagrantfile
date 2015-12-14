# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|
  config.vm.box = "ubuntu/trusty64"

  #   Expose Ports
  config.vm.network "forwarded_port", guest: 27017, host: 27017 # MongoDB
  config.vm.network "forwarded_port", guest: 6379,  host: 6379  # Redis

  config.vm.provision "shell", inline: <<-SHELL

     sudo add-apt-repository ppa:chris-lea/redis-server
     sudo apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv 7F0CEB10
     sudo echo "deb http://repo.mongodb.org/apt/ubuntu trusty/mongodb-org/3.0 multiverse" >/etc/apt/sources.list.d/mongodb-org-3.0.list

     sudo apt-get update

     sudo apt-get install -y python-pip
     sudo pip install pymongo

     sudo apt-get install -y redis-server > /dev/null
     sudo sed -i -e 's/127.0.0.1/0.0.0.0/g' /etc/redis/redis.conf
     sudo service redis-server restart

     sudo apt-get install -y mongodb-org > /dev/null
     sudo sed -i -e 's/127.0.0.1/0.0.0.0/g' /etc/mongod.conf
     sudo service mongod restart

  SHELL
end
