#!/bin/bash

for state in `netstat -ano | findstr "9092"`
do
	if [ $state = 'LISTENING' ]; then
		./kafka/bin/windows/kafka-server-stop.bat
		echo 'Closing kafka-server'
		break
	fi
done

wait

./kafka/bin/windows/kafka-server-start.bat ./kafka/config/server.properties &