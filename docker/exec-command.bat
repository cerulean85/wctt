@echo off

SETLOCAL

ECHO "Input Container Name or ID"
SET /P container=

ECHO "Input Command"
SET /P command=

docker exec -it --privileged %container% sh -c "%command%"

ENDLOCAL




