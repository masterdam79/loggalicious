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

#TODO: Make args requited/optional
if args.ics_path is not None: 
    ics_path = args.ics_path.strip()
else:
    print "No value given, exiting, try again.."
    sys.exit(0)
date_from = args.date_range[0] if args.date_range is not None else date.today() - timedelta(1)
date_to = args.date_range[1] if args.date_range is not None else date.today() - timedelta(1)

print("File path for .ics file: %s, Starting date: %s, Ending: %s" % (ics_path,date_from,date_to))
#exit()

ics = open(ics_path,'rb')
gcal = Calendar.from_ical(ics.read())
for component in gcal.walk():
    try:
        if component.name == "VEVENT":
            print(component.get('summary'))
            # Date Time Start
            dtstart = component.get('dtstart')
            print dtstart.to_ical()

            # Date Time End
            dtend = component.get('dtend')
            print dtend.to_ical()
            # print(component.get('dtstamp'))

    except:
        print("\n\n\nOops!")
ics.close()
