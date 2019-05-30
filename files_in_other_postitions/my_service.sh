#!/bin/bash

#need to change the monitoring file path according to your requirements
if [ "$(ls -A /root/jupyter/data/)" == "" ];then
  echo "empty"
else
  echo "not empty"
  rm -r /root/jupyter/data/*
fi

#need to change configuration file according to your environment
/root/redis/redis-4.0.14/src/redis-server

mongod -f /root/mongodb/data/mongodb.conf
