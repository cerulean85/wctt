@echo off

SETLOCAL

docker exec -it --privileged hadoop-master sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave1 sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave2 sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave3 sh -c "cd ~/; ./ready.sh"

ENDLOCAL




