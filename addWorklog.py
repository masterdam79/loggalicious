#!/usr/bin/env python3

import argparse
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

parser = argparse.ArgumentParser(description='Process some arguments.')

# A JIRA item
parser.add_argument('--jira_item', type=str)

# :param started: Moment when the work is logged, based on REST Browser it needs: "2014-06-03T08:21:01.273+0000"
parser.add_argument('--date', type=str)
parser.add_argument('--description', type=str)
parser.add_argument('--worked', type=str)

args = parser.parse_args()

for arg in vars(args):
    argvalue = getattr(args, arg)
    if str(argvalue) == 'None':
        print "No argument given for " + str(arg)
        exec(arg + " = raw_input('Give value for ' + arg + ': ')")
        #print eval(arg)
        if eval(arg) == "":
            print "No value given, exiting, try again.."
            sys.exit(0)
    else:
        exec(arg + " = argvalue")

jira.add_worklog(jira_item, timeSpent=worked)
