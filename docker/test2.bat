@echo off

SETLOCAL

SET /P data_directory=
SET image_name=zhwan85/hadoop-spark:latest

docker run -v %data_directory%:/data ^
               -p 8888:8888 -p 4040:4040 ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-master ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/data ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave1 ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/data ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave2 ^
               %image_name% tail -f /dev/null

docker run -v %data_directory%:/data ^
               --add-host master:172.17.0.2 ^
               --add-host slave1:172.17.0.3 ^
               --add-host slave2:172.17.0.4 ^
               --add-host slave3:172.17.0.5 ^
               -itd ^
               --restart always ^
               --name hadoop-slave3 ^
               %image_name% tail -f /dev/null

docker ps -a

ENDLOCAL




