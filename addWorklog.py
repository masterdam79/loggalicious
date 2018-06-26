#!/usr/bin/env python3

import configparser
from jira import JIRA
from jira.resources import Worklog

# Get some variables outside this script
config = configparser.ConfigParser()
config.read('./config.txt')
jira_user = config['BASICAUTH']['JIRA_USER']
jira_pass = config['BASICAUTH']['JIRA_PASS']
jira_url = config['BASICAUTH']['JIRA_URL']

jira = JIRA(basic_auth=(jira_user, jira_pass), options = {'server': jira_url})
issue = jira.issue('WSPORTAL-4238')

jira.add_worklog(issue, timeSpent='5h')
