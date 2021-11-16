#!/bin/bash

for state in `netstat -ano | findstr "2181"`
do
	if [ $state = 'LISTENING' ]; then
		./kafka/bin/windows/zookeeper-server-stop.bat
		echo 'Closing zookeeper-server'
		break
	fi
done

wait

./kafka/bin/windows/zookeeper-server-start.bat ./kafka/config/zookeeper.properties &