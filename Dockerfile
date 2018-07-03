FROM python:2

WORKDIR .

COPY . /application
RUN pip install jira configparser argparse icalendar tzlocal

COPY . .
