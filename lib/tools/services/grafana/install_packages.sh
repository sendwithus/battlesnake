#!/bin/bash

#
# collectd install
#
sudo apt-get update
sudo apt-get install collectd collectd-utils

# I'll copy my collectd config over the one installed.


#
# Install collectd-mongodb plugin
#

git clone https://github.com/sebest/collectd-mongodb.git
sudo mkdir /opt/collectd-mongodb
sudo chmod a+w /opt/collectd-mongodb

cp collectd-mongodb/mongodb.py /opt/collectd-mongodb
sudo cp collectd-mongodb/types.db /etc/collectd/


# Install InfluxDB
icurl -sL https://repos.influxdata.com/influxdb.key | sudo apt-key add -
source /etc/lsb-release
echo "deb https://repos.influxdata.com/${DISTRIB_ID,,} ${DISTRIB_CODENAME} stable" | sudo tee /etc/apt/sources.list.d/influxdb.list

sudo apt-get update && sudo apt-get install influxdb
sudo service influxdb start

influx -execute 'CREATE DATABASE collectd'
# create a 4 hour retention policy else queires get slow and time-out
influx -execute 'CREATE RETENTION POLICY four_hours ON collectd DURATION 4h REPLICATION 1 DEFAULT'

: <<__
# mods to indlux configs: /etc/influxdb/influxdb.conf

under [meta]
bind-address = ":8088" -> "0.0.0.0:8088"

under [admin]
bind-address = ":8083" -> "0.0.0.0:8083"

under  [http]
bind-address = ":8086" -> "0.0.0.0:8086"
# collectd stanza
[collectd]
  enabled = true
  bind-address = ":25826"
  database = "collectd"
  typesdb = "/usr/share/collectd/types.db"

__


# Grafana install
sudo echo 'deb https://packagecloud.io/grafana/stable/debian/ wheezy main' >> /etc/apt/sources.list
curl https://packagecloud.io/gpg.key | sudo apt-key add -

sudo apt-get update
sudo apt-get install grafana

: <<__
  You'll need to create a data source ... I don't see how to export it from grafana

  Name: battleSnake
  Type: InfluxDB 0.9.x
  Default: [check]
  Url: http://loclahost:8086

  IndluxDB Details
  database: collectd
  User: root
  Password: root

  And you can import the CPULoad-Dashboard.json as a Dashboard
__
