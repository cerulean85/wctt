#!/bin/bash 
 
/home/$USER/kafka/bin/kafka-topics.sh --delete --zookeeper localhost:2181 --topic $1

