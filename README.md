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

### How to install on Ubuntu
```
sudo apt update
sudo apt install python python-jira python-configparser python-argparse
```
