FROM python:2

WORKDIR .

COPY . /application
RUN pip install jira configparser argparse icalendar tzlocal
RUN echo "10.0.2.33 jira.ocom.com" >> /etc/hosts

COPY . .
