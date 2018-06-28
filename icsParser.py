#!/usr/bin/env python3
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import dateutil.parser
from dateutil.relativedelta import relativedelta
from pytz import UTC # timezone
import dateutil.parser
from pprint import pprint
import argparse
import re

# Parse CLI arguments
parser = argparse.ArgumentParser(description='Parse .ics file for calendar')
parser.add_argument('-f', '--ics_path', type=str, metavar='Ics-File-Path', required=True, help="Path to .ics file")
parser.add_argument('-d', '--date-range', nargs=2, metavar=('Start-Date','End-Date'),
                   help='start date and end date in YYYY-MM-DD formating (default: %s, %s)' %(date.today() - timedelta(1), date.today() - timedelta(1)))

args = parser.parse_args()

# Make args required/optional
if args.ics_path is not None:
    ics_path = args.ics_path.strip()
else:
    print "No value given, exiting, try again.."
    sys.exit(0)

# See if from/to date is given as argument, else default value to today
date_from = datetime.strptime(args.date_range[0], "%Y-%m-%d").date() if args.date_range is not None else date.today() # - timedelta(1)
date_to = datetime.strptime(args.date_range[1], "%Y-%m-%d").date() if args.date_range is not None else date.today() + timedelta(1)

class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

# Verbosity
print("File path for .ics file: %s, Starting date: %s, Ending: %s" % (ics_path,date_from,date_to))
#exit()

# Read file
ics = open(ics_path,'rb')
gcal = Calendar.from_ical(ics.read())

# Iterate over calendar events
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
                    jira_key_summary = re.search(regex, summary).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_summary)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
#                    python addWorklog.py --jira_item jira_key_summary --date date --worked duration.total_seconds() + "s" --description description
                elif re.search(regex, description):
                    print(bcolors.OKBLUE + 'Found a match in description!' + bcolors.ENDC)
                    jira_key_description = re.search(regex, description).group()
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
                    print("KEYS: " + jira_key_description)
                    print(bcolors.OKGREEN + '======matched======' + bcolors.ENDC)
#                    python addWorklog.py --jira_item jira_key_summary --date date --worked duration.total_seconds() + "s" --description description
                else:
                    print(bcolors.FAIL + 'You\'re not needed go away!' + bcolors.ENDC)


                print(bcolors.HEADER + '-------------------------' + bcolors.ENDC)


            except:
                print("\n")

ics.close()
