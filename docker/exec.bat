@echo off

SETLOCAL

SET /P container=

docker exec -it --privileged %container% bash

ENDLOCAL




