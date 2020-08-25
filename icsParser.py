#!/usr/bin/env python2.7
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import dateutil.parser
from dateutil.relativedelta import relativedelta
from pytz import UTC # timezone
import dateutil.parser
from pprint import pprint
import argparse
import re
from jira import JIRA
import configparser
from tzlocal import get_localzone
import urllib.request
import os
import shutil

'''
Get some variables outside this script
'''
config = configparser.ConfigParser()
config.read('./config.txt')
jira_user = config['BASICAUTH']['JIRA_USER']
jira_pass = config['BASICAUTH']['JIRA_PASS']
jira_url = config['BASICAUTH']['JIRA_URL']
ics_uri = config['OFFICE365']['ICS_URI']

'''
Some functions and classes
'''
# Function to check if jira item exists
def check_if_exists_jira_and_add_worklog(jira_item, date, duration, summary):
    try:
        issue = jira.issue(jira_item)
        print(jira_item)
        print(date)
        print(duration)
        print(str(summary))
        print(bcolors.UNDERLINE + issue.fields.project.key + bcolors.ENDC)
        print(bcolors.UNDERLINE + issue.fields.issuetype.name + bcolors.ENDC)
        print(bcolors.UNDERLINE + issue.fields.reporter.displayName + bcolors.ENDC)

        try:
            print("Trying to add worklog")
            jira_add_worklog(jira_item, date, duration, str(summary))
        except Exception as e1:
            print(bcolors.FAIL + 'Was unable to add worklog' + bcolors.ENDC)
            print(e1)
    except Exception as e2:
        print(bcolors.FAIL + 'No valid JIRA key item' + bcolors.ENDC)
        print(e2)


def jira_add_worklog(jira_item, date, duration, summary):
    print("Inside jira_add_worklog now")
    datetime_type = datetime.strptime(date, '%Y-%m-%d %H:%M')
    datetime_localized = tz.localize(datetime_type)
    if ", " in str(duration):
        print("Bigger than 1 day")
        days,time = str(duration).split(', ')
        days_int,days_str = str(days).split(' ')
        print(days_int)
        hours,minutes,seconds = str(time).split(':')
        duration_jira_readable = days_int + "d " + hours + "h " + minutes + "m"
    else:
        hours,minutes,seconds = str(duration).split(':')
        duration_jira_readable = hours + "h " + minutes + "m"

    print(duration_jira_readable)
    # https://jira.readthedocs.io/en/master/api.html#jira.JIRA.add_worklog
    jira.add_worklog(jira_item, timeSpent=duration_jira_readable, started=datetime_localized, comment=summary)

# Function to download file and display progress bar
def get_ics_file(url):
    # Download the file from `url` and save it locally under `file_name`:
    with urllib.request.urlopen(url) as response, open(file_name, 'wb') as out_file:
        shutil.copyfileobj(response, out_file)

# Class to add some color to the output
class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Class to parse arguments and show help if no required arguments are given
class MyParser(argparse.ArgumentParser):
    def error(self, message):
        sys.stderr.write('error: %s\n' % message)
        self.print_help()
        sys.exit(2)

'''
Initialize!!!
'''
parser = MyParser()
tz = get_localzone()
jira = JIRA(basic_auth=(jira_user, jira_pass), options = {'server': jira_url})

'''
Parse CLI arguments
'''
parser = argparse.ArgumentParser(description='Parse .ics file for calendar')
parser.add_argument('-f', '--ics_uri', type=str, metavar='Ics-File-URI', required=True, help="URI to .ics file")
parser.add_argument('-d', '--date-range', nargs=2, metavar=('Start-Date','End-Date'), help='start date and end date in YYYY-MM-DD formating (default: %s, %s)' %(date.today() - timedelta(1), date.today() - timedelta(1)))
args = parser.parse_args()

# See if from/to date is given as argument, else default value to today
date_from = datetime.strptime(args.date_range[0], "%Y-%m-%d").date() if args.date_range is not None else date.today() # - timedelta(1)
date_to = datetime.strptime(args.date_range[1], "%Y-%m-%d").date() if args.date_range is not None else date.today() + timedelta(1)

if 'https' in args.ics_uri:
    file_name = args.ics_uri.split('/')[-1]
    try:
        os.remove(file_name)
    except:
        print(bcolors.WARNING + "No " + file_name + " file here to delete." + bcolors.ENDC)
    get_ics_file(args.ics_uri)
    ics_file = file_name
else:
    ics_file = args.ics_uri

'''
Read the ics file
'''
# Verbosity
print("File path for .ics file: %s, Starting date: %s, Ending: %s" % (ics_file,date_from,date_to))
#exit()
ics = open(ics_file,'rb')
gcal = Calendar.from_ical(ics.read())

'''
Iterate over calendar events
'''
for component in gcal.walk():

    if component.name == "VEVENT":
        dtstart = component.decoded('dtstart')
        meeting_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart
        if (date_from <= meeting_date < date_to):
            try:
                status = component.decoded('X-MICROSOFT-CDO-BUSYSTATUS')
                # Put descriptive fields in variables
                print(bcolors.HEADER + "\n\n\n--------------New item--------------" + bcolors.ENDC)
                summary = component.decoded('summary')

#                print(type(component.get('description')))
                if component.get('description') is None: # The variable
                    print('It is None')
                    description = "No description available"
                else:
                    print ("It is defined and has a value")
                    description = component.decoded('description')

                print(bcolors.WARNING + "****** Calendar Item content ******" + bcolors.ENDC)
                print(summary)
                print(description)
                print(bcolors.WARNING + "****** Calendar Item content ******" + bcolors.ENDC)

                # Date Time Start
                dtstart = component.get('dtstart')
                #print dtstart.to_ical()
                start = component.decoded('dtstart')

                # Date Time End
                dtend = component.get('dtend')
                #print dtend.to_ical()
                end = component.decoded('dtend')
                duration = end - start

                print(duration.total_seconds())

                # Format date for parameter requirement
                date = str(start)[:16]
                print(date)

                # Define regex to match JIRA keys
                regex = r"[A-Z]+-[0-9]+"
                if re.search(regex, str(summary)):
                    print(bcolors.OKBLUE + 'Found a match in summary!' + bcolors.ENDC)
                    jira_key_from_summary = re.search(regex, str(summary)).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_from_summary)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    jira_item = jira_key_from_summary
                    if status.lower() == b'busy':
                        check_if_exists_jira_and_add_worklog(jira_item, date, duration, str(summary))
#                    python addWorklog.py --jira_item jira_key_from_summary --date date --worked duration.total_seconds() + "s" --description description
                elif re.search(regex, str(description)):
                    print(bcolors.OKBLUE + 'Found a match in description!' + bcolors.ENDC)
                    jira_key_from_description = re.search(regex, str(description)).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_from_description)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    jira_item = jira_key_from_description
                    if status.lower() == b'busy':
                        check_if_exists_jira_and_add_worklog(jira_item, date, duration, str(summary))
#                    python addWorklog.py --jira_item jira_key_from_summary --date date --worked duration.total_seconds() + "s" --description description
                else:
                    print(bcolors.FAIL + 'No regex matched' + bcolors.ENDC)

                print(bcolors.HEADER + '-------------------------' + bcolors.ENDC)

            except:
                print("\n")

'''
Close the ics file
'''
ics.close()
