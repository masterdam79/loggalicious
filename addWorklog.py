#!/usr/bin/env python3

import argparse
import configparser
from jira import JIRA
from jira.resources import Worklog
import sys
from datetime import datetime
from tzlocal import get_localzone

# Get some variables outside this script
config = configparser.ConfigParser()
config.read('./config.txt')
jira_user = config['BASICAUTH']['JIRA_USER']
jira_pass = config['BASICAUTH']['JIRA_PASS']
jira_url = config['BASICAUTH']['JIRA_URL']

tz = get_localzone()

jira = JIRA(basic_auth=(jira_user, jira_pass), options = {'server': jira_url})

class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

parser = MyParser()

# A JIRA item
parser.add_argument('-i', '--jira_item', type=str, metavar='JIRA Key', required=True, help="The JIRA key you want to log hours on, like ABC-123")

# :param started: Moment when the work is logged, based on REST Browser it needs: "2014-06-03T08:21:01.273+0000"
parser.add_argument('-d', '--date', type=str, metavar='Date', required=True, help="Format: 2018-06-28 18:00")
parser.add_argument('-n', '--description', type=str, metavar='Description', required=True, help="Fill in what you have done")
parser.add_argument('-w', '--worked', type=str, metavar='Time-Worked', required=True, help="Time worked, format: 2h, 1d")

args = parser.parse_args()

datetime = datetime.strptime(args.date, '%Y-%m-%d %H:%M')
datetime = tz.localize(datetime)


#exit(0)
# https://jira.readthedocs.io/en/master/api.html#jira.JIRA.add_worklog
jira.add_worklog(args.jira_item, timeSpent=args.worked, started=datetime, comment=args.description)
