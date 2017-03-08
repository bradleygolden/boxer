# boxer
pyenv and tox wrapped in docker.

boxer is batteries included python cli that manages python environments and tox for you. With boxer you no longer need to think about installing multiple versions of python and their dependencies. Simply run ```boxer``` and you have the power of [tox](https://tox.readthedocs.io/en/latest/) and [pyenv](https://github.com/pyenv/pyenv) at your fingertips.

## Why?

I was tired of repeating the pattern of setting up python environments and installing tox. I also wanted a way for my collegues to quickly test their code with little overhead.

boxer also serves as a useful tool during the CI process. With boxer, you can easily test your builds against multiple versions of python in a docker environment.

## How does it work?

Under the hood, boxer is using [docker-py](https://github.com/docker/docker-py), some existing images that I created on the Docker Hub, and the awesome [click](http://click.pocoo.org/5/) package. As you run the cli, a Dockerfile is created dynamically in the .boxer directory chained with a few images that I created for this project. boxer then builds the images created in the .boxer directory, runs them, and executes tox against your tox.ini.

Images on the Docker Hub:
* [docker-tox](https://hub.docker.com/r/bgolden/docker-tox/)
* [docker-pyenv](https://hub.docker.com/r/bgolden/docker-pyenv/)

## What you need:
* [docker](https://docs.docker.com/engine/installation/)
* [pip](https://pip.pypa.io/en/stable/installing/)
* connection to [docker hub](https://hub.docker.com/)

## Install
```
# $ pip install boxer  # soon
$ pip install git+https://github.com/bradleygolden/boxer.git
```

## Usage
```
$ cd <project/with/tox.ini>
$ boxer
```

## Python versions included

* 2.7.13
* 3.5.3
* 3.6.0
* 3.4.6

Alternatively, you can include more versions of python youself.

```
$ boxer -p 3.5.1 -p 3.4.4
```

## Example Output
```
Step 1/1 : FROM bgolden/docker-tox:latest
# Executing 3 build triggers...

Step 1/1 : COPY $BUILD_PATH /workspace
Step 1/1 : WORKDIR /workspace
Step 1/1 : CMD tox
---> Running in 7884d8ae4472
---> 0fef0fa44d49
Successfully built 0fef0fa44d49
GLOB sdist-make: /workspace/setup.py
py36 create: /workspace/.tox/py36
py36 installdeps: pytest
py36 inst: /workspace/.tox/dist/Example App-1.0.zip
py36 installed: appdirs==1.4.3,Example-App==1.0,packaging==16.8,py==1.4.32,pyparsing==2.2.0,pytest==3.0.6,six==1.10.0
py36 runtests: PYTHONHASHSEED='4201167492'
py36 runtests: commands[0] | pytest
============================= test session starts ==============================
platform linux -- Python 3.6.0, pytest-3.0.6, py-1.4.32, pluggy-0.4.0
rootdir: /workspace, inifile:
collected 1 items

test_app.py .

=========================== 1 passed in 0.01 seconds ===========================
___________________________________ summary ____________________________________
py36: commands succeeded
congratulations :)
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
