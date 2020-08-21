magic_scripts
===

run in docker
---
* install docker
* git clone `this project`
* cd `this project path`
* `docker build -t="duoduo3369/magic_scripts"` . (NOTICE: I change debain source.list to update download speed in china which write in Dockfile)
* start docker container: `docker run -it --rm --name magic_scripts -v "$PWD":/opt/projects/magic_scripts -w /opt/projects/magic_scripts duoduo3369/magic_scripts /bin/bash`
