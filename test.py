#!/usr/bin/env python2.7
import re
summary = "sometext [ABC-123] blaa"
regex = r"[A-Z]*-[0-9]*"
if re.search(regex, summary):
  print('found a match!')
  jira_key_summary = re.search(regex, summary).group()
  print("KEYS: " + jira_key_summary)
