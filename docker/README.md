# Dockerized Graphspace Python Client

## Steps Illustrated Below
- Build `graphspace-python` docker container
- Run `graphspace-python` docker image interactively and mount example data to container
- Run `graphspace-python` software on an example in this directory.

## Requirements
- Docker software
- Mac, linux, or Windows machine

## Build (Mac/Linux/Windows)

To build image: start from `graphspace-python` repository __root__ directory and call:

`docker build -t graphspace-python/graphspace-python -f docker/Dockerfile .`

To run the image interactively (with no linked data):

`docker run -it graphspace-python/graphspace-python bash`

## Run (Mac/Linux)

To mount the example data inside the container:

`docker run -v /$(pwd)/docker/example:/home/graphspace-python/example -it graphspace-python/graphspace-python bash`

then inside the container in the `/home/graphspace-python/example` directory call:

`python test.py example-graph.txt compbio@reed.edu compbio`

the output files will be linked to the host machine in the example subdirectory.

## Run (Windows) -- AR did not test.

To use the docker container with windows, use a bash terminal such as Git for Windows.

To run container in Git for Windows:

`winpty docker run -it graphspace-python/graphspace-python bash`

To run in Git for Windows and mount the example data inside the container:

`winpty docker run -v /$(pwd)/docker/example:/home/graphspace-python/example -it graphspace-python/graphspace-python bash`

then inside the container in the `/home/graphspace-python/example` directory call:

`python test.py example-graph.txt user6@example.com user6`
