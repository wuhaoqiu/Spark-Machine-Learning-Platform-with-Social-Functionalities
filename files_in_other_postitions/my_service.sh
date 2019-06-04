#!/bin/bash

#need to change the monitoring file path according to your requirements
if [ "$(ls -A /root/jupyter/data/)" == "" ];then
  echo "empty"
else
  echo "not empty"
  rm -r /root/jupyter/data/*
fi

#need to change configuration file according to your environment
#/root/redis/redis-4.0.14/src/redis-server

#mongod -f /root/mongodb/data/mongodb.conf

#bash $SPARK_HOME/bin/spark-submit /root/github/engr597-v3/engr597-stable/files_in_other_postitions/spark_task.py
