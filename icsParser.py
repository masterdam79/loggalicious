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
import urllib2
import os

'''
Get some variables outside this script
'''
config = configparser.ConfigParser()
config.read('./config.txt')
jira_user = config['BASICAUTH']['JIRA_USER']
jira_pass = config['BASICAUTH']['JIRA_PASS']
jira_url = config['BASICAUTH']['JIRA_URL']

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
        print(summary)
        print(bcolors.UNDERLINE + issue.fields.project.key + bcolors.ENDC)
        print(bcolors.UNDERLINE + issue.fields.issuetype.name + bcolors.ENDC)
        print(bcolors.UNDERLINE + issue.fields.reporter.displayName + bcolors.ENDC)

        try:
            print("Trying to add worklog")
            jira_add_worklog(jira_item, date, duration, summary)
        except:
            print(bcolors.FAIL + 'Was unable to add worklog' + bcolors.ENDC)
    except:
        print(bcolors.FAIL + 'No valid JIRA key item' + bcolors.ENDC)


def jira_add_worklog(jira_item, date, duration, summary):
    print("Inside add_worklog now")
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

# Fundtion to download file and display progress bar
def get_ics_file(url):
    u = urllib2.urlopen(url)
    f = open(file_name, 'wb')
    meta = u.info()
    file_size = int(meta.getheaders("Content-Length")[0])
    print "Downloading: %s Bytes: %s" % (file_name, file_size)

    file_size_dl = 0
    block_sz = 8192
    while True:
        buffer = u.read(block_sz)
        if not buffer:
            break

        file_size_dl += len(buffer)
        f.write(buffer)
        status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
        status = status + chr(8)*(len(status)+1)
        print status,

    f.close()

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
        print(bcolors.WARNING + "No " + file_name + " file here." + bcolors.ENDC)
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
                # Put descriptive fields in variables
                print(bcolors.HEADER + "\n\n\n--------------New item--------------" + bcolors.ENDC)
                summary = component.decoded('summary')
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

                print duration.total_seconds()

                # Format date for parameter requirement
                date = str(start)[:16]
                print(date)

                # Define regex to match JIRA keys
                regex = r"[A-Z]+-[0-9]+"

                if re.search(regex, summary):
                    print(bcolors.OKBLUE + 'Found a match in summary!' + bcolors.ENDC)
                    jira_key_from_summary = re.search(regex, summary).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_from_summary)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    check_if_exists_jira_and_add_worklog(jira_key_from_summary, date, duration, summary)
#                    python addWorklog.py --jira_item jira_key_from_summary --date date --worked duration.total_seconds() + "s" --description description
                elif re.search(regex, description):
                    print(bcolors.OKBLUE + 'Found a match in description!' + bcolors.ENDC)
                    jira_key_from_description = re.search(regex, description).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_from_description)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    check_if_exists_jira_and_add_worklog(jira_key_from_description, date, duration, summary)
#                    python addWorklog.py --jira_item jira_key_from_summary --date date --worked duration.total_seconds() + "s" --description description
                else:
                    print(bcolors.FAIL + 'You\'re not needed go away!' + bcolors.ENDC)


                print(bcolors.HEADER + '-------------------------' + bcolors.ENDC)


            except:
                print("\n")

'''
Close the ics file
'''
ics.close()
