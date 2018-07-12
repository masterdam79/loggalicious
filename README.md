# Loggalicious

## Introduction

These scripts are created to facilitate logging hours in Jira/Tempo using the python-jira package.

## Technology used

* Script: Python

## Dependencies

### Linux packages

* python
* python-pip

### PIP Install

* jira
* configparser
* argparse
* icalendar
* re

### Config file

* config.txt file in this directory containing the following variables:

```
[BASICAUTH]
JIRA_USER = <user>
JIRA_PASS = <pass>
JIRA_URL = <url>
JIRA_ITEM = <key>

```

**For some reason the config.txt needs a white line on the bottom**

**You can copy the .dist file and edit the configuration**

```
cp config.txt.dist config.txt
```

### How to install on Ubuntu
```
sudo apt update

sudo apt install python python-jira python-configparser python-argparse python-tzlocal
```

## Docker configuration

### Run the following commands:

```
sudo docker build -t loggalicious .

sudo docker run -td loggalicious /bin/bash

# If you have resolving issues you can use docker run --add-host <JIRA URL>:<JIRA IP> -td loggalicious /bin/bash

sudo docker ps

sudo docker exec -it <container identifier> bash

# Or CTID=$(sudo docker ps | grep loggalicious | awk '{print $1}') && sudo docker exec -it ${CTID} bash

# Once inside the container
cd application

python icsParser.py -f <full path to ics file>

(From - To date format) python icsParser.py -f <full path to ics file> -d YYYY-mm-dd YYYY-mm-dd

(From - To date formatexample:) python icsParser.py -f <full path to ics file> -d 2018-06-01 2018-06-30
```
