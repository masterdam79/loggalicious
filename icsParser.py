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

print(date_from)
print(date_to)


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
                print("\n\n\n\/ New item \/    \/ New item \/")
                summary = component.decoded('summary')
                description = component.decoded('description')
                print("****** Calendar Item content ******")
                print(summary)
                print(description)
                print("****** Calendar Item content ******")

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
                regex = r"[A-Z]*-[0-9]*"
#                regexp = re.compile(r'[A-Z]*\-[0-9]*', re.MULTILINE)
#                if (re.search(regex, summary) or re.search(regex, description)):
                if (re.search(regex, summary) or re.search(regex, description)):
                    print('found a match!')
#                if (re.search(regexp, summary) or re.search(regexp, description)):
                    jira_key_summary = re.search(regex, summary).group()
#                    jira_key_description = re.search(regex, description).group()
                    print '======matched======'
                    print("KEYS: " + jira_key_summary)
#                    print("KEYS: " + jira_key_summary + " - " + jira_key_description)
                    print '======matched======'
#                    python addWorklog.py --jira_item jira_key_summary --date date --worked duration.total_seconds() + "s" --description description

                print('-------------------------')


            except:
                print("\n")

ics.close()
