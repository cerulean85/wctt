@echo off
SETLOCAL

ECHO "Input Container Name or ID"
SET /P container=

docker commit %container% hadoop-spark
docker tag hadoop-spark zhwan85/hadoop-spark
docker push zhwan85/hadoop-spark

ENDLOCAL

