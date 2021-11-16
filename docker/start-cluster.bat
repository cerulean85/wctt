@echo off

SETLOCAL

SET data_directory=D:\__programming\jcoty\collected
SET image_name=zhwan85/hadoop-spark:latest

ECHO "DATA Dir: %data_directory%"
ECHO "Image Name: %image_name%"

docker run -v %data_directory%:/collected ^
               -p 8888:8888 -p 4040:4040 ^
               -e LC_ALL=C.UTF-8 ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-master ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/collected ^
               -e LC_ALL=C.UTF-8 ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave1 ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/collected ^
               -e LC_ALL=C.UTF-8 ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave2 ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/collected ^
               -e LC_ALL=C.UTF-8 ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave3 ^
               %image_name% tail -f /dev/null

docker exec -it --privileged hadoop-master sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave1 sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave2 sh -c "cd ~/; ./ready.sh"
docker exec -it --privileged hadoop-slave3 sh -c "cd ~/; ./ready.sh"

docker ps -a

ENDLOCAL




