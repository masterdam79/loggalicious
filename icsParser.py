#!/usr/bin/env python3
from icalendar import Calendar, Event
from datetime import date, datetime, timedelta
import dateutil.parser
from dateutil.relativedelta import relativedelta
from pytz import UTC # timezone
import dateutil.parser
from pprint import pprint
import argparse

# Parse CLI arguments
parser = argparse.ArgumentParser(description='Parse .ics file for calendar')
parser.add_argument('-f', '--ics_path', type=str, metavar='Ics-File-Path', required=True, help="Path to .ics file")
parser.add_argument('-d', '--date-range', nargs=2, metavar=('Start-Date','End-Date'),
                   help='start date and end date in YYYY-MM-DD formating (default: %s, %s)' %(date.today() - timedelta(1), date.today() - timedelta(1)))

args = parser.parse_args()

# Make args requited/optional
if args.ics_path is not None:
    ics_path = args.ics_path.strip()
else:
    print "No value given, exiting, try again.."
    sys.exit(0)
date_from = datetime.strptime(args.date_range[0], "%Y-%m-%d").date()  if args.date_range is not None else date.today() # - timedelta(1)
date_to = datetime.strptime(args.date_range[1], "%Y-%m-%d").date() if args.date_range is not None else date.today() + timedelta(1)

print("File path for .ics file: %s, Starting date: %s, Ending: %s" % (ics_path,date_from,date_to))
#exit()

ics = open(ics_path,'rb')
gcal = Calendar.from_ical(ics.read())
for component in gcal.walk():

    if component.name == "VEVENT":
        dtstart = component.decoded('dtstart')
        meeting_date = dtstart.date() if isinstance(dtstart, datetime) else dtstart
        if (date_from <= meeting_date < date_to):
            try:
                #pprint(component)
                print component.get('summary')
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
                print(start)

                # Logic to see if component.get('summary') or component.get('description') contains a JIRA key


            except:
                print("\n*")

ics.close()
