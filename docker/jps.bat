@echo off

SETLOCAL

ECHO "JPS: HADOOP MASTER"
docker exec -it --privileged hadoop-master sh -c "jps"

ECHO "JPS: HADOOP SLAVE 1"
docker exec -it --privileged hadoop-slave1 sh -c "jps"

ECHO "JPS: HADOOP SLAVE 2"
docker exec -it --privileged hadoop-slave2 sh -c "jps"

ECHO "JPS: HADOOP SLAVE 3"
docker exec -it --privileged hadoop-slave3 sh -c "jps"

ENDLOCAL




