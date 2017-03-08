# boxer
pyenv and tox wrapped in docker.

boxer is python cli that manages python environments with tox for you. With boxer you no longer need to install multiple python versions. Simply run ```boxer``` and all python versions are ready to be ran against tox.

## What you need:
* [docker](https://docs.docker.com/engine/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* connection to [docker hub](https://hub.docker.com/)

## Install
```
$ pip install boxer
```

## Usage
```
$ cd <project/with/tox.ini>
$ boxer
```

Alternatively, you can include a specific versions of python.

```
$ boxer -p 3.5.1 -p 3.4.4
```

## Help
```
$ boxer --help

Usage: boxer [OPTIONS]

 
  Example script.
 
Options:
  --project TEXT       Directory where your tox project is located
  --image TEXT         Tox docker image you wish to use to run with boxer
  --logs TEXT          Path to boxer log file
  --boxer TEXT         Path to store boxer data
  --dockerfile TEXT    Path to dockerfile
  --dockerignore TEXT  Path to dockerignore file
  --tag TEXT           Name of container tag saved by boxer
  --tox-file TEXT      Path to tox file
  -p, --python TEXT    Additional python versions to use (e.g. 2.7.13)
  --help               Show this message and exit.
```
